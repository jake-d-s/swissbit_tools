import JUtil as JU
import os
from tkinter import filedialog, messagebox
import tkinter.ttk
import re
import sys


def get_Serial_Num(filename):
    serial_num = JU.get_ASCII_string_from_DM_ASCII_file(filename, 4, 23, print_string=False)
    return serial_num


def get_Model_Num(filename):
    model_num = JU.get_ASCII_string_from_DM_ASCII_file(filename, 24, 63, print_string=False)
    return model_num


def get_FW_Rev(filename):
    fw_rev = JU.get_ASCII_string_from_DM_ASCII_file(filename, 64, 71, print_string=False)
    return fw_rev


def main():
    root = tkinter.Tk()
    root.withdraw()

    while (True):
        root.filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                   title='Select BEFORE Test Log Page 02 (SMART)',
                                                   filetypes=(('text files', '*.txt'), ('all files', '*.*')))
        # if we don't get a filename just bail
        if root.filename:
            idfy_file = root.filename
        else:
            exit(0)

        serial_num = get_Serial_Num(idfy_file)
        model_num = get_Model_Num(idfy_file)
        fw_rev = get_FW_Rev(idfy_file)

        print(serial_num + "," + model_num + "," + fw_rev)
        JU.wait()


if (__name__ == "__main__"):
    main()
