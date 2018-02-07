import sys
import os
import msvcrt
import colorama
from colorama import Fore, Back, Style
import datetime
import re
 
class Kbd:
    UP      = (True, 72)
    DOWN    = (True, 80)
    LEFT    = (True, 75)
    RIGHT   = (True, 77)
    ENTER   = 13
    ESC     = 27
    SPEC_ORD = 224

    def getArrow():
        while (not msvcrt.kbhit()):
            pass #Wait
        
        char = msvcrt.getch()
        ord_char = ord(char)

        if(ord_char == Kbd.ESC):
            abandonShip()
        elif(ord_char == Kbd.SPEC_ORD):
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

    def getKey():
        
        while (not msvcrt.kbhit()):
            pass #Wait
        
        char = msvcrt.getch()
        ord_char = ord(char)

        if(ord_char == Kbd.ESC):
            abandonShip()
        elif(ord_char == Kbd.SPEC_ORD):
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

    def printKeyOrd():
    
        while (not msvcrt.kbhit()):
            pass #Wait
            
        while (msvcrt.kbhit()):
            print(ord(msvcrt.getch()))
        
    
	
class Menu:

    def __init__ (self, titlesList):
    
        self.menuItems = []
        self.selected = Fore.GREEN + Style.NORMAL
        self.unselected = Fore.BLUE + Style.NORMAL
        self.chosen = Fore.RED + Style.BRIGHT
        self.chosenAndSelected = Fore.YELLOW + Style.BRIGHT
        self.header = ""
        self.currSelection = 0
        self.scrollWindowSize = (20 - 1) #written this way because index from 0
        self.endScroll = 0
        self.scrollWindowTop = 0
        self.scrollWindowBottom = self.scrollWindowSize
        counter = 0
  
        for title in titlesList:
            if(title[0:3] == "***"):
                self.endScroll = counter
            else:
                self.menuItems.append([title, False]) #[Display Name, Chosen]
                counter += 1

    def scrollWindow(self):
        if(self.currSelection < self.scrollWindowTop):
            self.scrollWindowTop = self.currSelection
            self.scrollWindowBottom = self.scrollWindowSize
        elif(self.currSelection >= self.endScroll):
            self.scrollWindowBottom = self.endScroll
            self.scrollWindowTop = self.endScroll - self.scrollWindowSize - 1
        elif(self.currSelection > self.scrollWindowBottom):
            self.scrollWindowBottom = self.currSelection
            self.scrollWindowTop = self.endScroll - self.scrollWindowSize - 1
			
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
                (index > self.scrollWindowBottom and
                 index < self.endScroll)):
                pass
            
            elif (index == currSel):
                if (self.isChosen(index)):
                    print(self.chosenAndSelected + self.option(index))
                else:
                    print(self.selected + self.option(index))
					
            elif (self.isChosen(index)): #Chosen
                print(self.chosen + self.option(index))
				
            else:
                print(self.unselected + self.option(index))

    def execute(self):
        print(self.unselected)
        os.system('cls')

    def isChosen(self, index):
        return self.menuItems[index][1]

    def option(self, index):
        return self.menuItems[index][0]                    
    
    def toggleChosen(self, index):
        if(self.menuItems[index][1]):
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
        while(keepRunning):
            key = Kbd.getKey()

            if (key == Kbd.UP):

                while(True):
                    self.currSelection -= 1
                    if (self.currSelection < 0):
                        self.currSelection = len(self.menuItems) - 1
                    if (self.menuItems[self.currSelection][0] != ""):
                        break
                self.update()

            if (key == Kbd.DOWN):
                while(True):
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
                keepRunning = False    
                
        self.execute()        
        
        return self.menuItems[self.currSelection][0]

    def generateMenuFile(filePath,options,commands):
        f = open(filePath, "w")
        for i in range(len(options)):
            f.write(options[i] + "\n")
            f.write(commands[i] + "\n")
        f.close()

    def generateEmptyCommand(toKeepRunning=True):
        if(toKeepRunning):
            command = ">stack.append(True)"
        else:
            command = ">stack.append(False)"
        return command


def little_endian_str_to_int(string):
    new_str = ""
    if (len(string) % 2 == 1):
        string += "0"
    index = len(string) - 1
    while (index > 0):
        new_str += string[index - 1] + string[index]
        index -= 2
    new_int = int(new_str, 16)
    return new_int
        
def datetime_to_str_until_minute():
    time = datetime.datetime.today()
    time_str = ""
    time_str += (str(time.month) + "/" + str(time.day) + "/" + str(time.year))
    time_str += (" " + str(time.hour).rjust(2,"0") + ":" + str(time.minute).rjust(2,"0"))
    return time_str
    
        
def abandonShip(exitString="The Program will now close, Good Bye!"):
    print(Style.RESET_ALL)
    os.system('cls')
    print(exitString)
    sys.exit()

def displayByPath(filepath):
    file = open(filepath, "r")
    text = file.read()
    file.close()
    print(text)
    Menu.wait()

def readList(listString):
    listString = listString.lstrip("[")
    listString = listString.rstrip("]")
    splitList = listString.split(",")
    for i in range(len(splitList)):
        splitList[i] = eval(splitList[i])
    return splitList
        
def Path(name,kind="main",folder=False):             
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
    
def fixSingleSlash(pathString):

    newString = []
    for char in pathString:
        newString.append(char)
        if (char == '\\'):
            newString.append(char)
    pathString = ''.join(newString)
    return pathString

def loadingDots(numDots=1, waitTime=.23):

    sys.stdout.write(". ")
    sleep(waitTime)
    if (numDots > 1):
        loadingDots(numDots - 1)

def wait():
    print("\nPress ENTER to continue")
    continueWaiting = True
    while(continueWaiting):
        if(Kbd.getKey() == Kbd.ENTER):
            continueWaiting = False

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
        if ("Block" in line):
            data = re.search("LBA= ([0-9]+) ", line)
            if (data):
                lba = data.group(1)
        else:
            data = re.search("^([0-9A-F]+) ", line)
            if (data):
                line_label = data.group(1)
                line_label = int(line_label, 16) + (512 * int(lba))
                if (target_byte < (line_label + 16)):
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
    if (print_hex):
        print(total)
    return total
    
def get_ASCII_string_from_DM_ASCII_file(filename, first_address, last_address, print_string=True):
    total = ""
    for i in range(first_address, last_address + 1):
        new_byte = get_byte_from_DM_ASCII_file(filename, i)
        total += chr(int(new_byte, 16))
    if (print_string):
        print(total)
    return total
    
def initialize():
    colorama.init()
    print(colorama.Back.WHITE)
            
if (__name__ == "__main__"):
    Kbd.printKeyOrd()