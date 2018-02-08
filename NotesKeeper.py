import msvcrt
import colorama
import os
import sys
import getopt
import traceback
from time import sleep
from colorama import Fore, Back, Style


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
            Utilities.abandon_ship()
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
            Utilities.abandon_ship()
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


class Menu:

    def __init__(self, filepath):
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

        option = []  # [Display Name, Chosen, Command 0,...,Command n]
        counter = 0
        f = open(filepath, "r")
        first_option = True
        for line in f:
            if not first_option:
                if line[0] == '>':
                    option.append(line.lstrip('>').rstrip('\n'))
                elif line[0:3] == "***":
                    self.endScroll = counter
                else:
                    self.menuItems.append(option)
                    option = [line.rstrip('\n'), False]
                    counter += 1
            if first_option:
                option.append(line.rstrip('\n'))
                option.append(False)
                first_option = False
                counter += 1
        if option:
            self.menuItems.append(option)
        f.close()

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
        command_list = self.menuItems[self.currSelection]
        print(self.unselected)
        os.system('cls')
        for i in range(len(command_list) - 2):
            exec(command_list[i + 2])

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
                self.execute()
                keep_running = False

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

    @staticmethod
    def wait():
        print("\nPress ENTER to continue")
        continue_waiting = True
        while continue_waiting:
            if Kbd.get_key() == Kbd.ENTER:
                continue_waiting = False


class Notes:

    def __init__(self, title, tags, path):
        self.title = title
        self.tags = tags
        self.path = path

    def get_path(self):
        return self.path

    def delete(self):
        print(self.path)
        Menu.wait()
        os.remove(eval("\"" + self.path + "\""))

    @staticmethod
    def fix(filepath):
        file = open(filepath, "r")
        new_note = Notes("Title", [], filepath)

        filetext = file.read()
        print(filetext)
        print('\n\n')
        new_note.title = input("Give the above note a title: ")
        add_tags = True
        menu = Menu(Utilities.path("fix_addTags", "menu"))
        while add_tags:
            menu.run()  # will push boolean for addTags, then the new tag
            new_tag = stack.pop()
            add_tags = stack.pop()
            if add_tags:
                new_note.tags.append(new_tag)

        file.close()
        new_string = []
        for char in filepath:
            new_string.append(char)
            if char == '\\':
                new_string.append(char)
        filepath = ''.join(new_string)
        file = open(filepath, "w")
        file.write("TITLE:" + new_note.title + "\n")
        file.write("TAGS:" + str(new_note.tags) + "\n")
        file.write("PATH:" + filepath + "\n\n")
        file.write(filetext)

    def display(self):
        add_tag = 0
        delete_note = 1
        return_to_menu = 2

        menu_file = Utilities.path("display", "menu")
        display_menu = Menu(menu_file)

        file = open(self.path, "r")
        text = file.read()
        file.close()

        display_menu.set_header(text + "\n")
        display_menu.run()
        instruction = stack.pop()

        if instruction == add_tag:
            self.add_tag()
            NotesList.populate_note_list()
        elif instruction == delete_note:
            pass
        elif instruction == return_to_menu:
            pass  # will drop back to main menu

    def add_tag(self):
        add_tags = True
        menu = Menu(Utilities.path("fix_addTags", "menu"))
        while add_tags:
            menu.run()  # will push boolean for addTags, then the new tag
            new_tag = stack.pop()
            add_tags = stack.pop()
            if add_tags:
                self.tags.append(new_tag)
        with open(self.path, "r") as f:
            text = f.readlines()
        text[1] = "TAGS:" + str(self.tags) + "\n"
        with open(self.path, "w") as f:
            for line in text:
                f.write(line)


class Tag:

    def __init__(self, title):
        self.title = title.upper()
        self.selected = False

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def is_equal(self, title):
        return self.title == title.upper()

    def get_title(tag):
        return tag.title


class NotesList:

    def __init__(self):
        self.masterNotesList = []
        self.masterTagList = []
        self.workingNotesList = []
        self.andTags = True
        self.orTags = False
        self.notTags = False

    def get_note_by_path(self, path):
        check_double_slash = path.split("\\")
        if check_double_slash[1] != '':
            path = Utilities.fix_single_slash(path)
        chosen_note = None
        for note in self.masterNotesList:
            if note.path == path:
                chosen_note = note
        if chosen_note:
            return chosen_note

    def sort_lists(self):
        self.masterNotesList.sort(key=Notes.get_path)
        self.workingNotesList.sort(key=Notes.get_path)

    def set_AND_tags(self):
        self.andTags = True
        self.orTags = False
        self.notTags = False

    def set_OR_tags(self):
        self.andTags = False
        self.orTags = True
        self.notTags = False

    def set_NOT_tags(self):
        self.andTags = False
        self.orTags = False
        self.notTags = True

    def toggle_tag_selected(self, index):
        self.masterTagList[index].selected = not self.masterTagList[index].selected

    def clear_tag_selected(self):
        for i in range(len(self.masterTagList)):
            self.masterTagList[i].selected = False

    def fill_master_notes_list(self):
        # Clear Master Notes List
        self.masterNotesList = []
        # Read Master List
        file = open(masterNoteList, "r")
        lines = []
        for line in file:
            lines.append(line.rstrip("\n"))
        file.close()

        for i in range(len(lines) // 3):
            new_note = Notes(lines[i * 3],
                             Utilities.read_list(lines[i * 3 + 1]),
                             lines[i * 3 + 2])
            self.masterNotesList.append(new_note)

        self.fill_tag_list()

    def populate_working_list(self):
        self.workingNotesList = []
        selected_tags = []

        for tag in self.masterTagList:
            if tag.selected:
                selected_tags.append(tag)

        if self.andTags:
            self.workingNotesList = self.masterNotesList
            if len(selected_tags) == 0:
                self.workingNotesList = []
            for tag in selected_tags:
                temp_list = []
                for note in self.workingNotesList:
                    for noteTag in note.tags:
                        if tag.is_equal(noteTag):
                            temp_list.append(note)
                self.workingNotesList = temp_list

        elif self.orTags:
            self.workingNotesList = []
            temp_list = []
            for tag in selected_tags:
                for note in self.masterNotesList:
                    for noteTag in note.tags:
                        if tag.is_equal(noteTag):
                            temp_list.append(note)
            for note in temp_list:
                not_duplicate = True
                for existingNote in self.workingNotesList:
                    if note.title == existingNote.title:
                        not_duplicate = False
                if not_duplicate:
                    self.workingNotesList.append(note)

        elif self.notTags:
            self.workingNotesList = []
            temp_list = []
            for tag in selected_tags:
                for note in self.masterNotesList:
                    for noteTag in note.tags:
                        if tag.is_equal(noteTag):
                            temp_list.append(note)
            for note in temp_list:
                not_duplicate = True
                for existingNote in self.workingNotesList:
                    if note.path == existingNote.path:
                        not_duplicate = False
                if not_duplicate:
                    self.workingNotesList.append(note)
            temp_list = []
            for note in self.masterNotesList:
                is_ORed_note = False
                for ORedNote in self.workingNotesList:
                    if note.path == ORedNote.path:
                        is_ORed_note = True
                if not is_ORed_note:
                    temp_list.append(note)
            self.workingNotesList = temp_list
        self.sort_lists()

    @staticmethod
    def populate_note_list():
        # Clear masterNoteList .txt file
        note_list_file = open(masterNoteList, "w")
        note_list_file.close()
        filepath = Utilities.path("", "note", folder=True)
        notes = []
        files = os.listdir(filepath)
        for file in files:
            if file[-4] != '.':
                folderfiles = os.listdir(filepath + file + "\\")
                for folderfile in folderfiles:
                    files.append(file + "\\" + folderfile)
            elif file[-4:] == ".txt":
                f = open((filepath + file), "r")
                title = f.readline()
                tags = f.readline()
                path = Utilities.fix_single_slash(filepath + file) + "\n"
                f.close()
                if title[:5] != "TITLE" or tags[:4] != "TAGS":
                    Notes.fix(filepath + file)
                    f = open((filepath + file), "r")
                    title = f.readline()
                    tags = f.readline()
                    f.close()
                notes.append(Notes(title[6:], tags[5:], path))
        note_list_file = open(masterNoteList, "w")
        for item in notes:
            note_list_file.write(item.title)
            note_list_file.write(str(item.tags))
            note_list_file.write(item.path)
        note_list_file.close()
        notesList.fill_master_notes_list()

    def select_note_from_list(self, use_master_list=True):
        if use_master_list:
            notes = self.masterNotesList
            header = "\n      NOTES\n"
        else:
            notes = self.workingNotesList
            header = "\n   TAGGED NOTES\n"

        # Create Menu
        menu_path = Utilities.path("menu_selectNoteFromList", "menu")
        file = open(menu_path, "w")
        path_selected = False
        for note in notes:
            file.write(note.title + "\n")
            file.write(">stack.append(\"" + note.path + "\")\n")
            file.write(">stack.append(True)\n")
        file.write(Menu.mark_end_scroll())
        file.write("\n")
        file.write(">stack.append(False)\n")
        file.write("Sort By Tags\n")
        file.write(">notesList.listByTags()\n")
        file.write(">stack.append(True)\n")
        file.close()

        menu = Menu(menu_path)
        menu.set_header(header)

        while not path_selected:
            menu.run()
            path_selected = stack.pop()

        chosen_path = stack.pop()
        chosen_note = notesList.get_note_by_path(chosen_path)

        if use_master_list:
            chosen_note.display()
        else:
            stack.append(chosen_path)

    def fill_tag_list(self):

        tag_list = []
        for note in self.masterNotesList:
            for tag in note.tags:
                duplicate_tag = False
                new_tag = Tag(tag)
                for listedTag in tag_list:
                    if listedTag.title == new_tag.title:
                        duplicate_tag = True
                if not duplicate_tag:
                    tag_list.append(new_tag)

        tag_list.sort(key=Tag.get_title)

        self.masterTagList = tag_list

    def list_by_tags(self):
        notesList.clear_tag_selected()
        title_list = []
        for tag in self.masterTagList:
            title_list.append(str(tag))

        command_list = []
        for i in range(len(title_list)):
            command_list.append(">self.toggleChosen(" + str(i) + ")\n"
                                                                ">notesList.toggleTagSelected(" + str(i) + ")\n"
                                                                                                           ">stack.append(True)")
        title_list.append(Menu.mark_end_scroll())
        command_list.append(Menu.generate_empty_command())
        title_list.append("AND Tags")
        command_list.append(">notesList.setAndTags()\n"
                           ">self.setChosen(-4)\n"
                           ">self.clrChosen(-3)\n"
                           ">self.clrChosen(-2)\n"
                           ">stack.append(True)")
        title_list.append("OR Tags")
        command_list.append(">notesList.setOrTags()\n"
                           ">self.clrChosen(-4)\n"
                           ">self.setChosen(-3)\n"
                           ">self.clrChosen(-2)\n"
                           ">stack.append(True)")
        title_list.append("NOT Tags")
        command_list.append(">notesList.setNotTags()\n"
                           ">self.clrChosen(-4)\n"
                           ">self.clrChosen(-3)\n"
                           ">self.setChosen(-2)\n"
                           ">stack.append(True)")
        title_list.append("Display Notes")
        command_list.append(">stack.append(False)")

        menu_file = Utilities.path("menu_listByTags", "menu")
        Menu.generate_menu_file(menu_file, title_list, command_list)

        menu = Menu(menu_file)
        menu.set_chosen(-4)

        keep_running = True
        while keep_running:
            notesList.populate_working_list()
            header = "   SELECT TAGS TO SEARCH\n\n"
            header += ("There are " + str(len(notesList.workingNotesList)) +
                       " notes that match your search\n")
            menu.set_header(header)
            menu.run()
            keep_running = stack.pop()

        notesList.select_note_from_list(False)

    def take_out_the_trash(self):
        for note in self.masterNotesList:
            kill_note = False
            for tag in note.tags:
                if tag.lower() == "garbage":
                    kill_note = True
            if kill_note:
                note.delete()

        NotesList.populate_note_list()


class Utilities:

    @staticmethod
    def abandon_ship(exit_string="The Program will now close, Good Bye!"):
        print(Style.RESET_ALL)
        os.system('cls')
        print(exit_string)
        sys.exit()

    @staticmethod
    def display_by_path(filepath):
        file = open(filepath, "r")
        text = file.read()
        file.close()
        print(text)
        Menu.wait()

    @staticmethod
    def read_list(list_string):
        list_string = list_string.lstrip("[")
        list_string = list_string.rstrip("]")
        split_list = list_string.split(",")
        for i in range(len(split_list)):
            split_list[i] = eval(split_list[i])
        return split_list

    @staticmethod
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

    @staticmethod
    def fix_single_slash(path_string):

        new_string = []
        for char in path_string:
            new_string.append(char)
            if char == '\\':
                new_string.append(char)
        path_string = ''.join(new_string)
        return path_string

    @staticmethod
    def loading_dots(num_dots=1, wait_time=.23):
        sys.stdout.write(". ")
        sleep(wait_time)
        if num_dots > 1:
            Utilities.loading_dots(num_dots - 1)


def initialize_notes_keeper(quick_boot, short_wait, long_wait):
    if quick_boot:
        global stack
        stack = []

        colorama.init()
        print(Fore.BLUE)
        print(Back.WHITE)
        os.system('cls')

        global masterNoteList
        masterNoteList = Utilities.path("masterNoteList")

        global notesList
        notesList = NotesList()

        NotesList.populate_note_list()

    else:
        # I don't know why colorama.init() lets me print one . at a time
        # but it does, so it's up here now.
        # This whole loading sequence is for show anyway haha  :)
        colorama.init()

        print("Booting NotesKeeper ")
        Utilities.loading_dots(6, short_wait)
        print("[ OK ]\n\n")
        sleep(long_wait)

        print("Initializing Stack ")
        Utilities.loading_dots(6, short_wait)
        print("[ OK ]\n\n")
        sleep(long_wait)

        print("Loading Color ")
        print(Fore.RED, end="")
        Utilities.loading_dots(wait_time=short_wait)
        print(Fore.YELLOW, end="")
        Utilities.loading_dots(wait_time=short_wait)
        print(Fore.BLUE, end="")
        Utilities.loading_dots(wait_time=short_wait)
        print(Fore.GREEN, end="")
        Utilities.loading_dots(wait_time=short_wait)
        print(Fore.MAGENTA, end="")
        Utilities.loading_dots(wait_time=short_wait)
        print(Fore.CYAN, end="")
        Utilities.loading_dots(wait_time=short_wait)
        print(Style.RESET_ALL, end="")
        print("[ " + Fore.GREEN + "OK" +
              Style.RESET_ALL + " ]\n\n")
        sleep(long_wait)

        print("Creating MASTER Note List ")
        Utilities.loading_dots(6, short_wait)
        print("[ " + Fore.GREEN + "OK" +
              Style.RESET_ALL + " ]\n\n")
        sleep(long_wait)

        print("Populating MASTER Note List ")
        Utilities.loading_dots(6, short_wait)
        print("[ " + Fore.GREEN + "OK" +
              Style.RESET_ALL + " ]\n\n")
        sleep(long_wait)

        print("Launching MAIN MENU ")
        Utilities.loading_dots(4)
        print(Back.WHITE + Fore.BLUE, end="")

        # This prevents conflict between quick and slow boots. Shh
        initialize_notes_keeper(True, short_wait, long_wait)


def main(argv):
    # Global Variables
    global stack
    global masterNoteList
    global notesList
    # Arguments
    quick_boot = False
    debug = False
    try:
        opts, args = getopt.getopt(argv, "hqd", ["help", "quick", "debug"])
    except getopt.GetoptError:
        error_string = ("ERROR: Unacceptable Arguments\n" +
                       "Acceptable Arguments: NotesKeeper.py " +
                       "[-h, --help] [-q, --quick] [-d, --debug]")
        Utilities.abandon_ship(error_string)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            Utilities.abandon_ship("Acceptable Arguments: " +
                                  "NotesKeeper.py [-h, --help]" +
                                  " [-q, --quick] [-d, --debug]")
        elif opt in ("-q", "--quick"):
            quick_boot = True
        elif opt in ("-d", "--debug"):
            debug = True

    # Initialize
    initialize_notes_keeper(quick_boot, .23, .5)

    # Run
    menu = Menu(Utilities.path("mainMenu", "menu"))
    menu.set_header("\n        MAIN MENU\n")

    while True:
        if debug:
            try:
                menu.run()
            except Exception:
                print(Style.RESET_ALL)
                os.system('cls')
                error_string = traceback.format_exc()
                sys.stdout.write(error_string)
                Menu.wait()
                sys.exit()
        else:
            try:
                menu.run()

            except Exception:
                error_string = ("Something Has Gone Wrong, NotesKeeper " +
                               "Terminating\n\nTo help Jake chase errors " +
                               "run as NotesKeeper.py -d")
                Utilities.abandon_ship(error_string)


if __name__ == "__main__":
    main(sys.argv[1:])
