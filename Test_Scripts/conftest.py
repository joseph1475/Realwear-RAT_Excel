import pytest
import time, datetime
from appium import webdriver
from appium.webdriver.appium_service import AppiumService


# removing environmental variable details
# From HTML report generated
def pytest_configure(config):
    config._metadata = None


# Adding screenshot to HTML report
# Only if a failure occurs
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
            Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
            :param item:
            """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    appium_service = AppiumService()
    appium_service.start()
    desired_caps1 = {
        "automationName": "UiAutomator2",  # Appium (default), or UiAutomator2
        "platformName": "Android",  # Andriod,IOS
        "platformVersion": "",  # can be open type or can declare the version .Eg: 8.1.1
        "deviceName": ""  # Android Emulator or 903e900a device ID
    }
    driver1 = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps1)
    driver1.implicitly_wait(10)
    driver1.get_screenshot_as_file(name)
    driver1.quit()
    time.sleep(5)

"""For generating HTML report"""


def pytest_cmdline_preparse(args):
    ts_report = time.time()
    time_stamp_report = datetime.datetime.fromtimestamp(ts_report).strftime('-%d-%m-%Y-%H-%M-%S')
    html_file = "Test_Report"+time_stamp_report+".html"
    print('HTML report file:', html_file)
    args.extend(['--tb=line', '--html', html_file, '--self-contained-html'])

# can be used in jenkins for passing path at run time
# def pytest_addoption(parser):
#     parser.addoption(
#         "--path", action="store", default=""
#     )
#     parser.addoption(
#         "--all", action="store", default=""
#     )
#
#
# @pytest.fixture()
# def setup(request):
#     path = request.config.getoption("--path")
#     #gbl.my_data['my_path'] = path
#     request.cls.path = path
#     all_excel = request.config.getoption("--all")
#     request.cls.all_excel = all_excel
#     # data = request.config.cache.get('my_path',None)
#     # data = {'my_path':path}
#     # request.config.cache.set('my_path',data)
#     # return data


# path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"

# @pytest.mark.usefixtures("setup")
# def get_sheet_names(setup):
#     print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#     path = setup
#     # path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"
#     command_df = pd.read_excel(path, None, header=0)
#     sheet_names = list(command_df.keys())
#     return sheet_names
