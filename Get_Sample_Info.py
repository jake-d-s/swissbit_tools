import JUtil as Ju
import os
from tkinter import filedialog
import tkinter.ttk



def get_serial_num(filename):
    serial_num = Ju.get_ASCII_string_from_DM_ASCII_file(filename, 4, 23, print_string=False)
    return serial_num


def get_model_num(filename):
    model_num = Ju.get_ASCII_string_from_DM_ASCII_file(filename, 24, 63, print_string=False)
    return model_num


def get_FW_rev(filename):
    fw_rev = Ju.get_ASCII_string_from_DM_ASCII_file(filename, 64, 71, print_string=False)
    return fw_rev


def main():
    root = tkinter.Tk()
    root.withdraw()

    while True:
        root.filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                   title='Select IDFY Ascii dump',
                                                   filetypes=(('text files', '*.txt'), ('all files', '*.*')))
        # if we don't get a filename just bail
        if root.filename:
            idfy_file = root.filename
        else:
            exit(0)

        serial_num = get_serial_num(idfy_file)
        model_num = get_model_num(idfy_file)
        fw_rev = get_FW_rev(idfy_file)

        print(serial_num + "," + model_num + "," + fw_rev)
        Ju.wait()


if __name__ == "__main__":
    main()
