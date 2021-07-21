import os
import re
import inspect
import logging
import subprocess
import time, datetime
import pandas as pd
import pytest
import xlsxwriter
from appium import webdriver
from playsound import playsound
from appium.webdriver.appium_service import AppiumService
from selenium.common.exceptions import NoSuchElementException

global row
global col

#@pytest.mark.usefixtures("setup")   #can be used with jenkins
class BaseClass:
    def getLogger(self):
        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)
        fileHandler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)  # filehandler object

        logger.setLevel(logging.DEBUG)
        return logger

    def sheet_runner(self, sheet, worksheet, path, workbook):
        self.close_recent_applications()
        log = self.getLogger()
        try:
            excel_df = pd.read_excel(path, sheet_name=sheet, header=0)
            #log.info(f"Reading commands of sheet {sheet}")
            print(f"Reading commands of sheet {sheet}")

            for row in range(len(excel_df.index)):
                cell_obj = excel_df.loc[row, 'Command']  # Vc from excel
                # verification_before(cell_obj)            #verifying voice commands before playing audio file
                delay = excel_df.loc[row, 'Delay']  # delay fro excel
                verification_text = excel_df.loc[row, 'Verification']
                self.voice_commands(cell_obj, worksheet, sheet, workbook)
                #log.info("delay applied between commands")
                time.sleep(delay)
                # verification_after(cell_obj)             #verifying voice commands after playing audio file
                self.verification(verification_text)
        except Exception as e:
            raise e

    def voice_commands(self, text, worksheet, sheet, workbook):
        log = self.getLogger()
        global row
        global col
        adb_clear = "adb shell logcat -c"
        os.system(adb_clear)
        adb_devinfo = "adb shell getprop ro.product.version.software"
        adb_process = subprocess.Popen(adb_devinfo, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        adb_bspversion = adb_process.communicate()[0]
        adb_bspversion = adb_bspversion.decode("utf-8")
        adb_platform = re.search(r'^\w+', str(adb_bspversion)).group(0)

        try:
            playsound('Tones/' + text + '.wav')
            time.sleep(1)
        except:
            playsound('Tones/' + text + '.mp3')
            time.sleep(1)
        ts = time.time()
        time_stamp = datetime.datetime.fromtimestamp(ts).strftime('-%d-%m-%Y-%H-%M-%S')
        adb_screenshot = "adb exec-out screencap -p > Screenshots/\"" + sheet + "\"/\"" + text + "\"" + time_stamp + ".png"
        os.system(adb_screenshot)
        adb_fetch = "adb shell logcat -d | find \"(ACCEPTED)\""
        adb_ps = subprocess.Popen(adb_fetch, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        adb_result = adb_ps.communicate()[0]
        adb_result = adb_result.decode("utf-8")
        try:
            adb_confidence = re.search(r"\[(.*?)\]", adb_result).group(1)
            adb_timestamp = re.search(r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}", adb_result).group(0)
            adb_result = re.search(r"\)(.*?)\[", adb_result).group(1)
        except AttributeError:
            adb_result = ""
            adb_confidence = ""
            adb_timestamp = ""
        adb_result = adb_result[1:-1]
        if text.lower() == adb_result.lower():
            print("" + text + " -> PASS")
            #log.info("" + text + " -> PASS")
            assert adb_result.lower() == text.lower()
            worksheet.write(row, col, adb_timestamp)
            worksheet.write(row, col + 1, adb_platform)
            worksheet.write(row, col + 2, adb_bspversion)
            worksheet.write(row, col + 3, text)
            worksheet.write(row, col + 4, adb_result)
            worksheet.write(row, col + 5, adb_confidence)
            worksheet.write(row, col + 6, "PASS")
            row += 1
        else:
            print("" + text + " -> FAIL")
            #log.info("" + text + " -> FAIL")
            worksheet.write(row, col, adb_timestamp)
            worksheet.write(row, col + 1, adb_platform)
            worksheet.write(row, col + 2, adb_bspversion)
            worksheet.write(row, col + 3, text)
            worksheet.write(row, col + 4, adb_result)
            worksheet.write(row, col + 5, adb_confidence)
            worksheet.write(row, col + 6, "FAIL")
            row += 1
            workbook.close()
            assert adb_result.lower() == text.lower(), "Voice command failed"

    def close_recent_applications(self):
        try:
            time.sleep(3)
            playsound('Tones/Recent Applications.wav')
            time.sleep(3)
            playsound('Tones/Dismiss All.wav')
            time.sleep(3)
            playsound('Tones/Navigate Back.wav')
            time.sleep(3)
        except:
            time.sleep(3)
            playsound('Tones/Recent Applications.mp3')
            time.sleep(3)
            playsound('Tones/Dismiss All.mp3')
            time.sleep(3)
            playsound('Tones/Navigate Back.mp3')
            time.sleep(3)

    def verification(self, verification_text):
        log=self.getLogger()
        text_skip = "skip"  # skipping verification if text matches skip
        text_reboot = "Reboot"
        #text_skip = verification_text  # skipping complete verification
        if text_skip == verification_text:
            #log.info("verification skipped")
            print("verification skipped")
            return True
        elif text_reboot == verification_text:
            print("Rebooting device")
            adb_reboot = "adb reboot"
            os.system(adb_reboot)
            time.sleep(60)
            print("Reboot completed")
            return True
        print(verification_text + ": Verification in progress")
        #log.info(verification_text + ": Verification in progress")
        appium_service = AppiumService()
        appium_service.start()  # start appium server

        desired_caps1 = {
            "automationName": "UiAutomator2",  # Appium (default), or UiAutomator2
            "platformName": "Android",  # Andriod,IOS
            "platformVersion": "",  # can be open type or can declare the version .Eg: 8.1.1
            "deviceName": ""  # Android Emulator or 903e900a device ID
        }
        driver1 = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps1)
        driver1.implicitly_wait(10)
        try:
            # checking if UI element is displayed on app list
            try:
                VoiceCommand = driver1.find_element_by_android_uiautomator(
                    f'new UiSelector().textContains("{verification_text}")').text
                assert VoiceCommand.upper() == verification_text.upper()
                print("Verification success")
                #log.info("Verification success")
            except:
                # if not displayed ,scrolling and selecting the item
                driver1.find_element_by_android_uiautomator(
                    "new UiScrollable(new UiSelector().resourceId(\"com.realwear.launcher:id/list2\"))"
                    ".setAsHorizontalList().scrollIntoView(" + f"new UiSelector().textContains(\"{verification_text}\"))")
                VoiceCommand = driver1.find_element_by_android_uiautomator(
                    f'new UiSelector().textContains("{verification_text}")').text
                assert VoiceCommand.upper() == verification_text.upper()
                print("Verification success")
                #log.info("Verification success")

        except NoSuchElementException:
            assert False, "Verification failed"
        finally:
            driver1.quit()
            time.sleep(5)

    # def verification_after(self, text):
    #     appium_service = AppiumService()
    #     appium_service.start()  # start appium server
    #     desired_caps1 = {
    #         "automationName": "UiAutomator2",  # Appium (default), or UiAutomator2
    #         "platformName": "Android",  # Andriod,IOS
    #         "platformVersion": "",  # can be open type or can declare the version .Eg: 8.1.1
    #         "deviceName": ""  # Android Emulator or 903e900a device ID
    #     }
    #     driver1 = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps1)
    #     driver1.implicitly_wait(10)
    #     text_dict = {'Navigate Home': 'MY PROGRAMS',
    #                  'My Controls': 'FLASHLIGHT',
    #                  'Recent Applications': 'DISMISS AL',
    #                  }
    #     try:
    #         if text in text_dict.keys():
    #             print(text + ": Verification after playing VC - in progress")
    #             verification_point = text_dict.get(text)
    #             # print(verification_point)
    #             VoiceCommand = driver1.find_element_by_android_uiautomator(
    #                 f'new UiSelector().textContains("{verification_point}")').text
    #             # print(VoiceCommand)
    #             assert VoiceCommand.upper() == verification_point.upper(), "Verification failed"
    #             print("Verification success")
    #
    #     except NoSuchElementException:
    #         assert False, "Verification failed"
    #
    #     finally:
    #         driver1.quit()
    #         time.sleep(5)
    #
    # def verification_before(self, text):
    #     text_skip = ('Navigate Home', 'Navigate Back',
    #                  'My Controls', 'Recent Applications', 'About Device')
    #     if text not in text_skip:
    #         print(text + ": Verification before playing VC - in progress")
    #         appium_service = AppiumService()
    #         appium_service.start()  # start appium server
    #         desired_caps1 = {
    #             "automationName": "UiAutomator2",  # Appium (default), or UiAutomator2
    #             "platformName": "Android",  # Andriod,IOS
    #             "platformVersion": "",  # can be open type or can declare the version .Eg: 8.1.1
    #             "deviceName": ""  # Android Emulator or 903e900a device ID
    #         }
    #         driver1 = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps1)
    #         driver1.implicitly_wait(10)
    #         try:
    #             VoiceCommand = driver1.find_element_by_android_uiautomator(
    #                 f'new UiSelector().textContains("{text}")').text
    #             assert VoiceCommand.upper() == text.upper()
    #             print("Verification success")
    #             # driver1.quit()
    #         except NoSuchElementException:
    #             assert False, "Verification failed"
    #
    #         finally:
    #             driver1.quit()
    #             time.sleep(5)

    def execute_cmd(self, sheet, path, sheet_runner):
        cwd = os.getcwd()
        reports = r'' + cwd + '/Reports/' + sheet + ''
        if not os.path.exists(reports):
            os.makedirs(reports)

        screenshots = r'' + cwd + '/Screenshots/' + sheet + ''
        if not os.path.exists(screenshots):
            os.makedirs(screenshots)
        global row
        global col
        row = 0
        col = 0
        ts_report = time.time()
        time_stamp_report = datetime.datetime.fromtimestamp(ts_report).strftime('-%d-%m-%Y-%H-%M-%S')
        workbook = xlsxwriter.Workbook("Reports/" + sheet + "/" + sheet + "" + time_stamp_report + ".xlsx")
        worksheet = workbook.add_worksheet()
        worksheet.write(row, col, "Time_Stamp")
        worksheet.write(row, col + 1, "Platform")
        worksheet.write(row, col + 2, "BSP_Version")
        worksheet.write(row, col + 3, "Expected")
        worksheet.write(row, col + 4, "Actual")
        worksheet.write(row, col + 5, "Confidence_Value")
        worksheet.write(row, col + 6, "Result")
        row += 1
        sheet_runner(sheet, worksheet, path, workbook)
        workbook.close()
