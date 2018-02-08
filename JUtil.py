import sys
import os
import msvcrt
import colorama
from colorama import Fore,  Style
from time import sleep
import datetime
import re


class Kbd:
    UP = (True, 72)
    DOWN = (True, 80)
    LEFT = (True, 75)
    RIGHT = (True, 77)
    ENTER = 13
    ESC = 27
    SPEC_ORD = 224

    @staticmethod
    def get_arrow():
        while not msvcrt.kbhit():
            pass  # Wait

        char = msvcrt.getch()
        ord_char = ord(char)

        if ord_char == Kbd.ESC:
            abandon_ship()
        elif ord_char == Kbd.SPEC_ORD:
            dr = ord(msvcrt.getch())

            if dr == Kbd.UP[1]:
                return Kbd.UP
            elif dr == Kbd.DOWN[1]:
                return Kbd.DOWN
            elif dr == Kbd.LEFT[1]:
                return Kbd.LEFT
            elif dr == Kbd.RIGHT[1]:
                return Kbd.RIGHT
            else:
                return Kbd.get_arrow()
        else:
            return Kbd.get_arrow()

    @staticmethod
    def get_key():

        while not msvcrt.kbhit():
            pass  # Wait

        char = msvcrt.getch()
        ord_char = ord(char)

        if ord_char == Kbd.ESC:
            abandon_ship()
        elif ord_char == Kbd.SPEC_ORD:
            dr = ord(msvcrt.getch())

            if dr == Kbd.UP[1]:
                return Kbd.UP
            elif dr == Kbd.DOWN[1]:
                return Kbd.DOWN
            elif dr == Kbd.LEFT[1]:
                return Kbd.LEFT
            elif dr == Kbd.RIGHT[1]:
                return Kbd.RIGHT
            else:
                return Kbd.get_key()
        else:
            return ord_char

    @staticmethod
    def print_key_ord():

        while not msvcrt.kbhit():
            pass  # Wait

        while msvcrt.kbhit():
            print(ord(msvcrt.getch()))


class Menu:

    def __init__(self, titles_list):

        self.menuItems = []
        self.selected = Fore.GREEN + Style.NORMAL
        self.unselected = Fore.BLUE + Style.NORMAL
        self.chosen = Fore.RED + Style.BRIGHT
        self.chosenAndSelected = Fore.YELLOW + Style.BRIGHT
        self.header = ""
        self.currSelection = 0
        self.scrollWindowSize = (20 - 1)  # written this way because index from 0
        self.endScroll = 0
        self.scrollWindowTop = 0
        self.scrollWindowBottom = self.scrollWindowSize
        counter = 0

        for title in titles_list:
            if title[0:3] == "***":
                self.endScroll = counter
            else:
                self.menuItems.append([title, False])  # [Display Name, Chosen]
                counter += 1

    def scroll_window(self):
        if self.currSelection < self.scrollWindowTop:
            self.scrollWindowTop = self.currSelection
            self.scrollWindowBottom = self.scrollWindowSize
        elif self.currSelection >= self.endScroll:
            self.scrollWindowBottom = self.endScroll
            self.scrollWindowTop = self.endScroll - self.scrollWindowSize - 1
        elif self.currSelection > self.scrollWindowBottom:
            self.scrollWindowBottom = self.currSelection
            self.scrollWindowTop = self.endScroll - self.scrollWindowSize - 1

    @staticmethod
    def mark_end_scroll():
        return "***\n"

    def clear_current_selection(self):
        self.currSelection = 0

    def str(self):
        return str(self.menuItems)

    def set_header(self, string):
        self.header = string

    def update(self):
        self.scroll_window()
        curr_sel = self.currSelection
        print(self.unselected)
        os.system('cls')
        print(self.header)

        for index in range(len(self.menuItems)):
            if (index < self.scrollWindowTop or
                    (self.scrollWindowBottom < index < self.endScroll)):
                pass

            elif index == curr_sel:
                if self.is_chosen(index):
                    print(self.chosenAndSelected + self.option(index))
                else:
                    print(self.selected + self.option(index))

            elif self.is_chosen(index):  # Chosen
                print(self.chosen + self.option(index))

            else:
                print(self.unselected + self.option(index))

    def execute(self):
        print(self.unselected)
        os.system('cls')

    def is_chosen(self, index):
        return self.menuItems[index][1]

    def option(self, index):
        return self.menuItems[index][0]

    def toggle_chosen(self, index):
        if self.menuItems[index][1]:
            self.menuItems[index][1] = False
        else:
            self.menuItems[index][1] = True

    def set_chosen(self, index):
        self.menuItems[index][1] = True

    def clr_chosen(self, index):
        self.menuItems[index][1] = False

    def run(self):
        self.update()
        keep_running = True
        while keep_running:
            key = Kbd.get_key()

            if key == Kbd.UP:

                while True:
                    self.currSelection -= 1
                    if self.currSelection < 0:
                        self.currSelection = len(self.menuItems) - 1
                    if self.menuItems[self.currSelection][0] != "":
                        break
                self.update()

            if key == Kbd.DOWN:
                while True:
                    self.currSelection += 1
                    if self.currSelection > (len(self.menuItems) - 1):
                        self.currSelection = 0
                    if self.menuItems[self.currSelection][0] != "":
                        break
                self.update()

            if key == Kbd.RIGHT:
                self.currSelection = len(self.menuItems) - 1
                self.update()

            if key == Kbd.LEFT:
                self.currSelection = 0
                self.update()

            if key == Kbd.ENTER:
                keep_running = False

        self.execute()

        return self.menuItems[self.currSelection][0]

    @staticmethod
    def generate_menu_file(file_path, options, commands):
        f = open(file_path, "w")
        for i in range(len(options)):
            f.write(options[i] + "\n")
            f.write(commands[i] + "\n")
        f.close()

    @staticmethod
    def generate_empty_command(to_keep_running=True):
        if to_keep_running:
            command = ">stack.append(True)"
        else:
            command = ">stack.append(False)"
        return command


def little_endian_str_to_int(string):
    new_str = ""
    if len(string) % 2 == 1:
        string += "0"
    index = len(string) - 1
    while index > 0:
        new_str += string[index - 1] + string[index]
        index -= 2
    new_int = int(new_str, 16)
    return new_int


def datetime_to_str_until_minute():
    time = datetime.datetime.today()
    time_str = ""
    time_str += (str(time.month) + "/" + str(time.day) + "/" + str(time.year))
    time_str += (" " + str(time.hour).rjust(2, "0") + ":" + str(time.minute).rjust(2, "0"))
    return time_str


def abandon_ship(exit_string="The Program will now close, Good Bye!"):
    print(Style.RESET_ALL)
    os.system('cls')
    print(exit_string)
    sys.exit()


def display_by_path(filepath):
    file = open(filepath, "r")
    text = file.read()
    file.close()
    print(text)
    Menu.wait()


def read_list(list_string):
    list_string = list_string.lstrip("[")
    list_string = list_string.rstrip("]")
    split_list = list_string.split(",")
    for i in range(len(split_list)):
        split_list[i] = eval(split_list[i])
    return split_list


def path(name, kind="main", folder=False):
    filepath = "C:\\py\\NotesKeeper\\"
    extension = ".txt"
    if kind == "note":
        filepath += "Notes\\"
    if kind == "menu":
        filepath += "Menus\\"

    if folder:
        return filepath
    else:
        return filepath + name + extension


def fix_single_slash(path_string):
    new_string = []
    for char in path_string:
        new_string.append(char)
        if char == '\\':
            new_string.append(char)
    path_string = ''.join(new_string)
    return path_string


def loading_dots(num_dots=1, wait_time=.23):
    sys.stdout.write(". ")
    sleep(wait_time)
    if num_dots > 1:
        loading_dots(num_dots - 1)


def wait():
    print("\nPress ENTER to continue")
    continue_waiting = True
    while continue_waiting:
        if Kbd.get_key() == Kbd.ENTER:
            continue_waiting = False


def get_byte_from_DM_ASCII_file(filename, target_byte):
    """
    Given the filepath to a saved DriveMaster ReadA buffer dump (saved in ASCII format)
    and a target byte address (relative to the top of the file) returns a string of the 
    byte in hexademcimal with no leading '0x' or trailing 'h'
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    lba = 0
    target_line = ""

    for line in lines:
        if "Block" in line:
            data = re.search("LBA= ([0-9]+) ", line)
            if data:
                lba = data.group(1)
        else:
            data = re.search("^([0-9A-F]+) ", line)
            if data:
                line_label = data.group(1)
                line_label = int(line_label, 16) + (512 * int(lba))
                if target_byte < (line_label + 16):
                    target_line = line
                    break

    line_chunks = target_line.split()
    target_index = (target_byte % 16) + 1
    targeted_byte = line_chunks[target_index]
    return targeted_byte


def get_little_endian_from_DM_ASCII_file(filename, first_address, last_address, print_hex=True):
    total = ""
    for i in range(last_address, (first_address - 1), -1):
        new_byte = get_byte_from_DM_ASCII_file(filename, i)
        total += new_byte
    if print_hex:
        print(total)
    return total


def get_ASCII_string_from_DM_ASCII_file(filename, first_address, last_address, print_string=True):
    total = ""
    for i in range(first_address, last_address + 1):
        new_byte = get_byte_from_DM_ASCII_file(filename, i)
        total += chr(int(new_byte, 16))
    if print_string:
        print(total)
    return total


def initialize():
    colorama.init()
    print(colorama.Back.WHITE)


if __name__ == "__main__":
    Kbd.print_key_ord()
