import pandas as pd
import pytest
import os
import re
from Test_Scripts.utilities.BaseClass import BaseClass


class TestOne(BaseClass):
    # all_excel = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts"
    # path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"
    #
    # if all_excel:
    #     excel_sheets =glob.glob(all_excel +'/*.xlsx')
    #     for sheet in excel_sheets:
    #
    # elif path:
    #     pass
    # # def get_sheet_names(self):
    # #     print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    # #
    # #     #path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"
    # #     command_df = pd.read_excel(self.path, None, header=0)
    # #     sheet_names = list(command_df.keys())
    # #     return sheet_names
    # all_excel = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts"
    print("//Enter The Excel Path:-")
    path = input("//Enter The Excel Path:-")  # input - requesting user input at run time
    for dirs in os.walk(path):
        excel_files = [pos_excel for pos_excel in os.listdir(dirs[0]) if pos_excel.endswith('.xlsx')]
        print(dirs[0])
        print(excel_files)
        sheet_names = []
    # path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"
        for excel_file in excel_files:
            sheet_path = os.path.join(path, excel_file)
            print(sheet_path)
            command_df = pd.read_excel(sheet_path, None, header=0)
            test_keys = command_df.keys()
            print(test_keys)
            for i in test_keys:
                sheet_names.append(i)
            #sheet_names = sheet_names.append(command_df.keys())
            print(sheet_names)
            # for sheets in sheet_names:
            #     print(sheets)
            # # @pytest.mark.parametrize("sheet_name", get_sheet_names())
            @pytest.mark.parametrize("sheet_name", sheet_names)
            def test_case(self, sheet_name):
                self.execute_cmd(sheet_name, self.path + "/" + re.sub(r'[0-9_]+', '', sheet_name) + ".xlsx", self.sheet_runner)
