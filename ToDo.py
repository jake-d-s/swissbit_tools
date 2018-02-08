import JUtil as Ju
import os
from colorama import Fore, Back, Style



class ToDo:
    unstarted = 0
    in_progress = 1
    done = 2
    admin = 3

    regression = "REGTEST"
    misc = "MISCELLANEOUS"

    def __init__(self, name, level=0):  # 0 = .unstarted
        self.name = name
        self.level = level

    def __str__(self):
        return self.name + "," + str(self.level)

    def progress(self):
        if self.level != ToDo.admin:
            self.level += 1
            self.name = "    " + self.name
            if self.level > ToDo.done:
                self.level = ToDo.unstarted
                self.name = self.name[12:]

    @staticmethod
    def progress_by_name(list_of_todos, name):
        for to_do in list_of_todos:
            if to_do.name == name:
                to_do.progress()

    def set_admin(self):
        self.level = ToDo.admin


class ToDoMenu(Ju.Menu):

    def __init__(self, to_do_list):

        self.menuItems = []
        self.unselected = Back.WHITE + Fore.BLUE + Style.NORMAL
        self.selected = Fore.CYAN + Style.BRIGHT
        self.unstarted = Fore.RED + Style.BRIGHT
        self.in_progress = Fore.YELLOW + Style.BRIGHT
        self.done = Fore.GREEN + Style.NORMAL
        self.header = ""
        self.currSelection = 0
        self.scrollWindowSize = (20 - 1)  # written this way because index from 0
        self.endScroll = 0
        self.scrollWindowTop = 0
        self.scrollWindowBottom = self.scrollWindowSize
        counter = 0

        for to_do in to_do_list:
            if to_do.name[0:3] == "***":
                self.endScroll = counter
            else:
                self.menuItems.append(to_do)
                counter += 1

        while self.option(self.currSelection) == "":
            self.currSelection += 1

    def get_level(self, index):
        return self.menuItems[index].level

    def option(self, index):
        return self.menuItems[index].name

    def run(self):
        self.update()
        keep_running = True
        while keep_running:
            key = Ju.Kbd.get_key()

            if key == Ju.Kbd.UP:

                while True:
                    self.currSelection -= 1
                    if self.currSelection < 0:
                        self.currSelection = len(self.menuItems) - 1
                    if self.option(self.currSelection) != "":
                        break
                self.update()

            if key == Ju.Kbd.DOWN:
                while True:
                    self.currSelection += 1
                    if self.currSelection > (len(self.menuItems) - 1):
                        self.currSelection = 0
                    if self.option(self.currSelection) != "":
                        break
                self.update()

            if key == Ju.Kbd.RIGHT:
                self.currSelection = len(self.menuItems) - 1
                self.update()

            if key == Ju.Kbd.LEFT:
                self.currSelection = 0
                self.update()

            if key == Ju.Kbd.ENTER:
                keep_running = False

        self.execute()

        return self.option(self.currSelection)

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
                print(self.selected + self.option(index))
            elif self.get_level(index) == ToDo.admin:
                print(self.unselected + self.option(index))
            elif self.get_level(index) == ToDo.unstarted:
                print(self.unstarted + self.option(index))
            elif self.get_level(index) == ToDo.in_progress:
                print(self.in_progress + self.option(index))
            elif self.get_level(index) == ToDo.done:
                print(self.done + self.option(index))

    def execute(self):
        print(self.unselected)
        os.system('cls')


def import_save_file(file_path, list_type):
    new_list = None
    valid_type = False
    if list_type == ToDo.regression:
        tag = ToDo.regression
        valid_type = True
    elif list_type == ToDo.misc:
        tag = ToDo.misc
        valid_type = True

    if valid_type:
        with open(file_path, "r") as f:
            lines = f.readlines()
        to_dos = []
        new_list = []

        for line in lines:
            new_line = line.rstrip("\n")
            new_line = new_line.split(",")
            to_dos.append(new_line)

        for to_do in to_dos:
            if to_do[0] == tag:
                for i in range(len(to_do) // 2):
                    new_to_do = ToDo(to_do[2 * i + 1], int(to_do[2 * i + 2]))
                    new_list.append(new_to_do)
    return new_list


def export_save_file(file_path, to_do_list, list_type):
    valid_type = False
    if list_type == ToDo.regression:
        tag = ToDo.regression
        index = 0
        valid_type = True
    elif list_type == ToDo.misc:
        tag = ToDo.misc
        index = 1
        valid_type = True

    if valid_type:
        with open(file_path, "r") as file:
            text = file.readlines()
        with open(file_path, "w") as file:
            output_line = tag
            for item in to_do_list:
                if item.level != ToDo.admin:
                    output_line += ","
                    output_line += item.name
                    output_line += ","
                    output_line += str(item.level)
            text[index] = output_line + "\n"
            file.write(''.join(text))


class MenuHandler:

    def __init__(self, save_file, tag):
        self.menu = None
        self.test_list = []
        self.tag = tag
        self.save_file = save_file

    def add_new_batch(self):
        fw_title = input("What Firmware Version Are You Testing?:\n >>> ")

        self.menu.menuItems.insert(-4, ToDo(fw_title.upper() + " LPO 8G SLC"))
        self.menu.menuItems.insert(-4, ToDo(fw_title.upper() + " LPO 480G MLC"))
        self.menu.menuItems.insert(-4, ToDo(fw_title.upper() + " fsync 8G SLC"))
        self.menu.menuItems.insert(-4, ToDo(fw_title.upper() + " fsync 50G 4PL"))
        self.menu.menuItems.insert(-4, ToDo(fw_title.upper() + " fsync 100G 4PL"))
        self.menu.menuItems.insert(-4, ToDo(fw_title.upper() + " fsync 200G MLC"))

    def clear_admin_tests(self):
        accumulator_list = []
        for to_do in self.test_list:
            if to_do.level != ToDo.admin:
                accumulator_list.append(to_do)
        self.test_list = accumulator_list

    def clear_finished_tests(self):
        working_tests = []
        for test in self.test_list:
            if test.level != ToDo.done:
                working_tests.append(test)
        self.test_list = working_tests

    def open_menu(self):

        self.test_list = import_save_file(self.save_file, self.tag)

        add_batch = "Add New Regression Test"
        clear_finished = "Clear Finished Tests"
        quit_program = "Quit"

        self.test_list.append(ToDo("", ToDo.admin))
        self.test_list.append(ToDo(add_batch, ToDo.admin))
        self.test_list.append(ToDo(clear_finished, ToDo.admin))
        self.test_list.append(ToDo(quit_program, ToDo.admin))
        self.menu = ToDoMenu(self.test_list)

        while True:
            selected_option = self.menu.run()

            if selected_option == add_batch:
                self.add_new_batch()
                self.menu.currSelection = 1
            elif selected_option == clear_finished:
                self.clear_finished_tests()
                self.menu = ToDoMenu(self.test_list)
            elif selected_option == quit_program:
                break
            else:
                ToDo.progress_by_name(self.menu.menuItems, selected_option)

        self.test_list = self.menu.menuItems
        self.clear_admin_tests()
        export_save_file(self.save_file, self.test_list, self.tag)


class MiscMenuHandler(MenuHandler):

    def add_new_batch(self):
        task_title = input("What task would you like to track?:\n >>> ")

        self.menu.menuItems.insert(-4, ToDo(task_title.upper()))

    def open_menu(self):

        self.test_list = import_save_file(self.save_file, self.tag)

        add_task = "Add New Task"
        clear_finished = "Clear Finished Tests"
        quit_program = "Quit"

        self.test_list.append(ToDo("", ToDo.admin))
        self.test_list.append(ToDo(add_task, ToDo.admin))
        self.test_list.append(ToDo(clear_finished, ToDo.admin))
        self.test_list.append(ToDo(quit_program, ToDo.admin))
        self.menu = ToDoMenu(self.test_list)

        while True:
            selected_option = self.menu.run()

            if selected_option == add_task:
                self.add_new_batch()
                self.menu.currSelection = 1
            elif selected_option == clear_finished:
                self.clear_finished_tests()
                self.menu = ToDoMenu(self.test_list)
            elif selected_option == quit_program:
                break
            else:
                ToDo.progress_by_name(self.menu.menuItems, selected_option)

        self.test_list = self.menu.menuItems
        self.clear_admin_tests()
        export_save_file(self.save_file, self.test_list, self.tag)


def main():
    Ju.initialize()

    save_file_path = "C:\\py\\ToDo\\SaveToDo.txt"

    regression_testing = "Regression Tests"
    misc_tasks = "Miscellaneous Tasks"
    quit_program = "Quit"

    main_menu_titles = [regression_testing, misc_tasks, quit_program]
    main_menu = Ju.Menu(main_menu_titles)
    main_menu.set_header("\n   TO DO   \n")

    reg_menu_handler = MenuHandler(save_file_path, ToDo.regression)
    misc_menu_handler = MiscMenuHandler(save_file_path, ToDo.misc)
    while True:
        selected_option = main_menu.run()

        if selected_option == regression_testing:
            reg_menu_handler.open_menu()
        if selected_option == misc_tasks:
            misc_menu_handler.open_menu()
        if selected_option == quit_program:
            break


if __name__ == "__main__":
    main()
