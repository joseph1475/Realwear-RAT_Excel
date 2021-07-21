import pandas as pd
import pytest
#from pathlib import Path
#import conftest

from Test_Scripts.utilities.BaseClass import BaseClass


#path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"

# @pytest.mark.usefixtures("setup")
# def get_sheet_names(request):
#     print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#     path = request.config.cache.get('my_path')
#     # path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"
#     command_df = pd.read_excel(path, None, header=0)
#     sheet_names = list(command_df.keys())
#     return sheet_names


class TestOne(BaseClass):
    # def get_sheet_names(self):
    #     print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    #
    #     #path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"
    #     command_df = pd.read_excel(self.path, None, header=0)
    #     sheet_names = list(command_df.keys())
    #     return sheet_names

    #path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"
    command_df = pd.read_excel(path, None, header=0)
    sheet_names = list(command_df.keys())

    #@pytest.mark.parametrize("sheet_name", get_sheet_names())
    @pytest.mark.parametrize("sheet_name",sheet_names)
    def test_case(self, sheet_name,path):
        path = self.path
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(path)
        self.execute_cmd(sheet_name,path, self.sheet_runner)


