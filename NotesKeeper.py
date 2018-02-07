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
    def getArrow():
        while (not msvcrt.kbhit()):
            pass  # Wait

        char = msvcrt.getch()
        ord_char = ord(char)

        if (ord_char == Kbd.ESC):
            Utilities.abandonShip()
        elif (ord_char == Kbd.SPEC_ORD):
            dr = ord(msvcrt.getch())

            if (dr == Kbd.UP[1]):
                return Kbd.UP
            elif (dr == Kbd.DOWN[1]):
                return Kbd.DOWN
            elif (dr == Kbd.LEFT[1]):
                return Kbd.LEFT
            elif (dr == Kbd.RIGHT[1]):
                return Kbd.RIGHT
            else:
                return Kbd.getArrow()
        else:
            return Kbd.getArrow()

    @staticmethod
    def getKey():

        while (not msvcrt.kbhit()):
            pass  # Wait

        char = msvcrt.getch()
        ord_char = ord(char)

        if (ord_char == Kbd.ESC):
            Utilities.abandonShip()
        elif (ord_char == Kbd.SPEC_ORD):
            dr = ord(msvcrt.getch())

            if (dr == Kbd.UP[1]):
                return Kbd.UP
            elif (dr == Kbd.DOWN[1]):
                return Kbd.DOWN
            elif (dr == Kbd.LEFT[1]):
                return Kbd.LEFT
            elif (dr == Kbd.RIGHT[1]):
                return Kbd.RIGHT
            else:
                return Kbd.getKey()
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
        firstOption = True
        for line in f:
            if (not firstOption):
                if (line[0] == '>'):
                    option.append(line.lstrip('>').rstrip('\n'))
                elif (line[0:3] == "***"):
                    self.endScroll = counter
                else:
                    self.menuItems.append(option)
                    option = [line.rstrip('\n'), False]
                    counter += 1
            if (firstOption):
                option.append(line.rstrip('\n'))
                option.append(False)
                firstOption = False
                counter += 1
        if (option):
            self.menuItems.append(option)
        f.close()

    def scrollWindow(self):
        if (self.currSelection < self.scrollWindowTop):
            self.scrollWindowTop = self.currSelection
            self.scrollWindowBottom = self.scrollWindowSize
        elif (self.currSelection >= self.endScroll):
            self.scrollWindowBottom = self.endScroll
            self.scrollWindowTop = self.endScroll - self.scrollWindowSize - 1
        elif (self.currSelection > self.scrollWindowBottom):
            self.scrollWindowBottom = self.currSelection
            self.scrollWindowTop = self.endScroll - self.scrollWindowSize - 1

    @staticmethod
    def markEndScroll():
        return "***\n"

    def clrCurrSel(self):
        self.currSelection = 0

    def str(self):
        return str(self.menuItems)

    def setHeader(self, string):
        self.header = string

    def update(self):
        self.scrollWindow()
        currSel = self.currSelection
        print(self.unselected)
        os.system('cls')
        print(self.header)

        for index in range(len(self.menuItems)):
            if (index < self.scrollWindowTop or
                    (self.scrollWindowBottom < index < self.endScroll)):
                pass

            elif (index == currSel):
                if (self.isChosen(index)):
                    print(self.chosenAndSelected + self.option(index))
                else:
                    print(self.selected + self.option(index))

            elif (self.isChosen(index)):  # Chosen
                print(self.chosen + self.option(index))

            else:
                print(self.unselected + self.option(index))

    def execute(self):
        commandList = self.menuItems[self.currSelection]
        print(self.unselected)
        os.system('cls')
        for i in range(len(commandList) - 2):
            exec(commandList[i + 2])

    def isChosen(self, index):
        return self.menuItems[index][1]

    def option(self, index):
        return self.menuItems[index][0]

    def toggleChosen(self, index):
        if (self.menuItems[index][1]):
            self.menuItems[index][1] = False
        else:
            self.menuItems[index][1] = True

    def setChosen(self, index):
        self.menuItems[index][1] = True

    def clrChosen(self, index):
        self.menuItems[index][1] = False

    def run(self):
        self.update()
        keepRunning = True
        while (keepRunning):
            key = Kbd.getKey()

            if (key == Kbd.UP):

                while (True):
                    self.currSelection -= 1
                    if (self.currSelection < 0):
                        self.currSelection = len(self.menuItems) - 1
                    if (self.menuItems[self.currSelection][0] != ""):
                        break
                self.update()

            if (key == Kbd.DOWN):
                while (True):
                    self.currSelection += 1
                    if (self.currSelection > (len(self.menuItems) - 1)):
                        self.currSelection = 0
                    if (self.menuItems[self.currSelection][0] != ""):
                        break
                self.update()

            if (key == Kbd.RIGHT):
                self.currSelection = len(self.menuItems) - 1
                self.update()

            if (key == Kbd.LEFT):
                self.currSelection = 0
                self.update()

            if (key == Kbd.ENTER):
                self.execute()
                keepRunning = False

    @staticmethod
    def generateMenuFile(filePath, options, commands):
        f = open(filePath, "w")
        for i in range(len(options)):
            f.write(options[i] + "\n")
            f.write(commands[i] + "\n")
        f.close()

    @staticmethod
    def generateEmptyCommand(toKeepRunning=True):
        if (toKeepRunning):
            command = ">stack.append(True)"
        else:
            command = ">stack.append(False)"
        return command

    @staticmethod
    def wait():
        print("\nPress ENTER to continue")
        continueWaiting = True
        while (continueWaiting):
            if (Kbd.getKey() == Kbd.ENTER):
                continueWaiting = False


class Notes:

    def __init__(self, title, tags, path):
        self.title = title
        self.tags = tags
        self.path = path

    def getPath(self):
        return self.path

    def delete(self):
        print(self.path)
        Menu.wait()
        os.remove(eval("\"" + self.path + "\""))

    @staticmethod
    def fix(filepath):
        file = open(filepath, "r")
        newNote = Notes("Title", [], filepath)

        filetext = file.read()
        print(filetext)
        print('\n\n')
        newNote.title = input("Give the above note a title: ")
        addTags = True
        menu = Menu(Utilities.Path("fix_addTags", "menu"))
        while (addTags):
            menu.run()  # will push boolean for addTags, then the new tag
            newTag = stack.pop()
            addTags = stack.pop()
            if (addTags):
                newNote.tags.append(newTag)

        file.close()
        newString = []
        for char in filepath:
            newString.append(char)
            if (char == '\\'):
                newString.append(char)
        filepath = ''.join(newString)
        file = open(filepath, "w")
        file.write("TITLE:" + newNote.title + "\n")
        file.write("TAGS:" + str(newNote.tags) + "\n")
        file.write("PATH:" + filepath + "\n\n")
        file.write(filetext)

    def display(self):
        add_tag = 0
        delete_note = 1
        return_to_menu = 2

        menu_file = Utilities.Path("display", "menu")
        display_menu = Menu(menu_file)

        file = open(self.path, "r")
        text = file.read()
        file.close()

        display_menu.setHeader(text + "\n")
        display_menu.run()
        instruction = stack.pop()

        if (instruction == add_tag):
            self.add_tag()
            NotesList.populateNoteList()
        elif (instruction == delete_note):
            pass
        elif (instruction == return_to_menu):
            pass  # will drop back to main menu

    def add_tag(self):
        addTags = True
        menu = Menu(Utilities.Path("fix_addTags", "menu"))
        while (addTags):
            menu.run()  # will push boolean for addTags, then the new tag
            newTag = stack.pop()
            addTags = stack.pop()
            if (addTags):
                self.tags.append(newTag)
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

    def isEqual(self, title):
        return (self.title == title.upper())

    def getTitle(tag):
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
        if (check_double_slash[1] != ''):
            path = Utilities.fixSingleSlash(path)
        chosen_note = None
        for note in self.masterNotesList:
            if (note.path == path):
                chosen_note = note
        if (chosen_note):
            return (chosen_note)

    def sortLists(self):
        self.masterNotesList.sort(key=Notes.getPath)
        self.workingNotesList.sort(key=Notes.getPath)

    def setAndTags(self):
        self.andTags = True
        self.orTags = False
        self.notTags = False

    def setOrTags(self):
        self.andTags = False
        self.orTags = True
        self.notTags = False

    def setNotTags(self):
        self.andTags = False
        self.orTags = False
        self.notTags = True

    def toggleTagSelected(self, index):
        self.masterTagList[index].selected = not self.masterTagList[index].selected

    def clearTagSelected(self):
        for i in range(len(self.masterTagList)):
            self.masterTagList[i].selected = False

    def fillMasterNotesList(self):
        # Clear Master Notes List
        self.masterNotesList = []
        # Read Master List
        file = open(masterNoteList, "r")
        lines = []
        for line in file:
            lines.append(line.rstrip("\n"))
        file.close()

        for i in range(len(lines) // 3):
            newNote = Notes(lines[i * 3],
                            Utilities.readList(lines[i * 3 + 1]),
                            lines[i * 3 + 2])
            self.masterNotesList.append(newNote)

        self.fillTagList()

    def populateWorkingList(self):
        self.workingNotesList = []
        selectedTags = []

        for tag in self.masterTagList:
            if (tag.selected):
                selectedTags.append(tag)

        if (self.andTags):
            self.workingNotesList = self.masterNotesList
            if (len(selectedTags) == 0):
                self.workingNotesList = []
            for tag in selectedTags:
                tempList = []
                for note in self.workingNotesList:
                    for noteTag in note.tags:
                        if (tag.isEqual(noteTag)):
                            tempList.append(note)
                self.workingNotesList = tempList

        elif (self.orTags):
            self.workingNotesList = []
            tempList = []
            for tag in selectedTags:
                for note in self.masterNotesList:
                    for noteTag in note.tags:
                        if (tag.isEqual(noteTag)):
                            tempList.append(note)
            for note in tempList:
                notDuplicate = True
                for existingNote in self.workingNotesList:
                    if (note.title == existingNote.title):
                        notDuplicate = False
                if (notDuplicate):
                    self.workingNotesList.append(note)

        elif (self.notTags):
            self.workingNotesList = []
            tempList = []
            for tag in selectedTags:
                for note in self.masterNotesList:
                    for noteTag in note.tags:
                        if (tag.isEqual(noteTag)):
                            tempList.append(note)
            for note in tempList:
                notDuplicate = True
                for existingNote in self.workingNotesList:
                    if (note.path == existingNote.path):
                        notDuplicate = False
                if (notDuplicate):
                    self.workingNotesList.append(note)
            tempList = []
            for note in self.masterNotesList:
                isORedNote = False
                for ORedNote in self.workingNotesList:
                    if (note.path == ORedNote.path):
                        isORedNote = True
                if (not isORedNote):
                    tempList.append(note)
            self.workingNotesList = tempList
        self.sortLists()

    @staticmethod
    def populateNoteList():
        # Clear masterNoteList .txt file
        noteListFile = open(masterNoteList, "w")
        noteListFile.close()
        filepath = Utilities.Path("", "note", folder=True)
        notes = []
        files = os.listdir(filepath)
        for file in files:
            if (file[-4] != '.'):
                folderfiles = os.listdir(filepath + file + "\\")
                for folderfile in folderfiles:
                    files.append(file + "\\" + folderfile)
            elif (file[-4:] == ".txt"):
                f = open((filepath + file), "r")
                title = f.readline()
                tags = f.readline()
                path = Utilities.fixSingleSlash(filepath + file) + "\n"
                f.close()
                if (title[:5] != "TITLE" or tags[:4] != "TAGS"):
                    Notes.fix(filepath + file)
                    f = open((filepath + file), "r")
                    title = f.readline()
                    tags = f.readline()
                    f.close()
                notes.append(Notes(title[6:], tags[5:], path))
        noteListFile = open(masterNoteList, "w")
        for item in notes:
            noteListFile.write(item.title)
            noteListFile.write(str(item.tags))
            noteListFile.write(item.path)
        noteListFile.close()
        notesList.fillMasterNotesList()

    def selectNoteFromList(self, useMasterList=True):
        if (useMasterList):
            notes = self.masterNotesList
            header = "\n      NOTES\n"
        else:
            notes = self.workingNotesList
            header = "\n   TAGGED NOTES\n"

        # Create Menu
        menuPath = Utilities.Path("menu_selectNoteFromList", "menu")
        file = open(menuPath, "w")
        pathSelected = False
        for note in notes:
            file.write(note.title + "\n")
            file.write(">stack.append(\"" + note.path + "\")\n")
            file.write(">stack.append(True)\n")
        file.write(Menu.markEndScroll())
        file.write("\n")
        file.write(">stack.append(False)\n")
        file.write("Sort By Tags\n")
        file.write(">notesList.listByTags()\n")
        file.write(">stack.append(True)\n")
        file.close()

        menu = Menu(menuPath)
        menu.setHeader(header)

        while (not pathSelected):
            menu.run()
            pathSelected = stack.pop()

        chosenPath = stack.pop()
        chosen_note = notesList.get_note_by_path(chosenPath)

        if (useMasterList):
            chosen_note.display()
        else:
            stack.append(chosenPath)

    def fillTagList(self):

        tagList = []
        for note in self.masterNotesList:
            for tag in note.tags:
                duplicateTag = False
                newTag = Tag(tag)
                for listedTag in tagList:
                    if (listedTag.title == newTag.title):
                        duplicateTag = True
                if (not duplicateTag):
                    tagList.append(newTag)

        tagList.sort(key=Tag.getTitle)

        self.masterTagList = tagList

    def listByTags(self):
        notesList.clearTagSelected()
        titleList = []
        for tag in self.masterTagList:
            titleList.append(str(tag))

        commandList = []
        for i in range(len(titleList)):
            commandList.append(">self.toggleChosen(" + str(i) + ")\n"
                                                                ">notesList.toggleTagSelected(" + str(i) + ")\n"
                                                                                                           ">stack.append(True)")
        titleList.append(Menu.markEndScroll())
        commandList.append(Menu.generateEmptyCommand())
        titleList.append("AND Tags")
        commandList.append(">notesList.setAndTags()\n"
                           ">self.setChosen(-4)\n"
                           ">self.clrChosen(-3)\n"
                           ">self.clrChosen(-2)\n"
                           ">stack.append(True)")
        titleList.append("OR Tags")
        commandList.append(">notesList.setOrTags()\n"
                           ">self.clrChosen(-4)\n"
                           ">self.setChosen(-3)\n"
                           ">self.clrChosen(-2)\n"
                           ">stack.append(True)")
        titleList.append("NOT Tags")
        commandList.append(">notesList.setNotTags()\n"
                           ">self.clrChosen(-4)\n"
                           ">self.clrChosen(-3)\n"
                           ">self.setChosen(-2)\n"
                           ">stack.append(True)")
        titleList.append("Display Notes")
        commandList.append(">stack.append(False)")

        menuFile = Utilities.Path("menu_listByTags", "menu")
        Menu.generateMenuFile(menuFile, titleList, commandList)

        menu = Menu(menuFile)
        menu.setChosen(-4)

        keepRunning = True
        while (keepRunning):
            notesList.populateWorkingList()
            header = ("   SELECT TAGS TO SEARCH\n\n")
            header += ("There are " + str(len(notesList.workingNotesList)) +
                       " notes that match your search\n")
            menu.setHeader(header)
            menu.run()
            keepRunning = stack.pop()

        notesList.selectNoteFromList(False)

    def takeOutTheTrash(self):
        for note in self.masterNotesList:
            killNote = False
            for tag in note.tags:
                if (tag.lower() == "garbage"):
                    killNote = True
            if (killNote):
                note.delete()

        NotesList.populateNoteList()


class Utilities:

    @staticmethod
    def abandonShip(exitString="The Program will now close, Good Bye!"):
        print(Style.RESET_ALL)
        os.system('cls')
        print(exitString)
        sys.exit()

    @staticmethod
    def displayByPath(filepath):
        file = open(filepath, "r")
        text = file.read()
        file.close()
        print(text)
        Menu.wait()

    @staticmethod
    def readList(listString):
        listString = listString.lstrip("[")
        listString = listString.rstrip("]")
        splitList = listString.split(",")
        for i in range(len(splitList)):
            splitList[i] = eval(splitList[i])
        return splitList

    @staticmethod
    def Path(name, kind="main", folder=False):
        filepath = "C:\\py\\NotesKeeper\\"
        extension = ".txt"
        if (kind == "note"):
            filepath += "Notes\\"
        if (kind == "menu"):
            filepath += "Menus\\"

        if (folder):
            return filepath
        else:
            return (filepath + name + extension)

    @staticmethod
    def fixSingleSlash(pathString):

        newString = []
        for char in pathString:
            newString.append(char)
            if (char == '\\'):
                newString.append(char)
        pathString = ''.join(newString)
        return pathString

    @staticmethod
    def loadingDots(numDots=1, waitTime=.23):
        sys.stdout.write(". ")
        sleep(waitTime)
        if (numDots > 1):
            Utilities.loadingDots(numDots - 1)


def initializeNotesKeeper(quickBoot, shortWait, longWait):
    if (quickBoot):
        global stack
        stack = []

        colorama.init()
        print(Fore.BLUE)
        print(Back.WHITE)
        os.system('cls')

        global masterNoteList
        masterNoteList = Utilities.Path("masterNoteList")

        global notesList
        notesList = NotesList()

        NotesList.populateNoteList()

    else:
        # I don't know why colorama.init() lets me print one . at a time
        # but it does, so it's up here now.
        # This whole loading sequence is for show anyway haha  :)
        colorama.init()

        print("Booting NotesKeeper ")
        Utilities.loadingDots(6, shortWait)
        print("[ OK ]\n\n")
        sleep(longWait)

        print("Initializing Stack ")
        Utilities.loadingDots(6, shortWait)
        print("[ OK ]\n\n")
        sleep(longWait)

        print("Loading Color ")
        print(Fore.RED, end="")
        Utilities.loadingDots(waitTime=shortWait)
        print(Fore.YELLOW, end="")
        Utilities.loadingDots(waitTime=shortWait)
        print(Fore.BLUE, end="")
        Utilities.loadingDots(waitTime=shortWait)
        print(Fore.GREEN, end="")
        Utilities.loadingDots(waitTime=shortWait)
        print(Fore.MAGENTA, end="")
        Utilities.loadingDots(waitTime=shortWait)
        print(Fore.CYAN, end="")
        Utilities.loadingDots(waitTime=shortWait)
        print(Style.RESET_ALL, end="")
        print("[ " + Fore.GREEN + "OK" +
              Style.RESET_ALL + " ]\n\n")
        sleep(longWait)

        print("Creating MASTER Note List ")
        Utilities.loadingDots(6, shortWait)
        print("[ " + Fore.GREEN + "OK" +
              Style.RESET_ALL + " ]\n\n")
        sleep(longWait)

        print("Populating MASTER Note List ")
        Utilities.loadingDots(6, shortWait)
        print("[ " + Fore.GREEN + "OK" +
              Style.RESET_ALL + " ]\n\n")
        sleep(longWait)

        print("Launching MAIN MENU ")
        Utilities.loadingDots(4)
        print(Back.WHITE + Fore.BLUE, end="")

        # This prevents conflict between quick and slow boots. Shh
        initializeNotesKeeper(True, shortWait, longWait)


def main(argv):
    # Global Variables
    global stack
    global masterNoteList
    global notesList
    # Arguments
    quickBoot = False
    debug = False
    try:
        opts, args = getopt.getopt(argv, "hqd", ["help", "quick", "debug"])
    except getopt.GetoptError:
        errorString = ("ERROR: Unacceptable Arguments\n" +
                       "Acceptable Arguments: NotesKeeper.py " +
                       "[-h, --help] [-q, --quick] [-d, --debug]")
        Utilities.abandonShip(errorString)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            Utilities.abandonShip("Acceptable Arguments: " +
                                  "NotesKeeper.py [-h, --help]" +
                                  " [-q, --quick] [-d, --debug]")
        elif opt in ("-q", "--quick"):
            quickBoot = True
        elif opt in ("-d", "--debug"):
            debug = True

    # Initialize
    initializeNotesKeeper(quickBoot, .23, .5)

    # Run
    menu = Menu(Utilities.Path("mainMenu", "menu"))
    menu.setHeader("\n        MAIN MENU\n")

    while (True):
        if (debug):
            try:
                menu.run()
            except Exception:
                print(Style.RESET_ALL)
                os.system('cls')
                errorString = traceback.format_exc()
                sys.stdout.write(errorString)
                Menu.wait()
                sys.exit()
        else:
            try:
                menu.run()

            except Exception:
                errorString = ("Something Has Gone Wrong, NotesKeeper " +
                               "Terminating\n\nTo help Jake chase errors " +
                               "run as NotesKeeper.py -d")
                Utilities.abandonShip(errorString)


if __name__ == "__main__":
    main(sys.argv[1:])
