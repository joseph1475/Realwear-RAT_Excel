import os
import glob

os.chdir(r'C:\Users\josep\OneDrive - RealWear\Desktop\Python_Excels\Excel_based_Scripts')
for excel in glob.glob('*.xlsx'):
    if excel == "AboutDevice.xlsx":
        print(excel)
    elif excel == "AudioRecorder.xlsx":
        print(excel)
    elif excel == "GlobalCommands.xlsx":
        print(excel)
    elif excel == "MyFiles.xlsx":
        print(excel)
