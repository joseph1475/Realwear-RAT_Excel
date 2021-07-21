import pandas as pd
import pytest

from Test_Scripts.utilities.BaseClass import BaseClass


# path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"

# @pytest.mark.usefixtures("setup")
# def get_sheet_names(setup):
#     print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#     path = setup
#     # path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"
#     command_df = pd.read_excel(path, None, header=0)
#     sheet_names = list(command_df.keys())
#     return sheet_names


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
    path = input("enter the excel path:-")
    # path = r"C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts\MyFiles.xlsx"
    # command_df = pd.read_excel(gbl.my_data['my_path'], None, header=0)
    command_df = pd.read_excel(path, None, header=0)
    sheet_names = list(command_df.keys())

    # @pytest.mark.parametrize("sheet_name", get_sheet_names())
    @pytest.mark.parametrize("sheet_name", sheet_names)
    def test_case(self, sheet_name):
        self.execute_cmd(sheet_name, self.path, self.sheet_runner)
