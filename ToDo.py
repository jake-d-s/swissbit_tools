import JUtil as JU
import sys
import os
import msvcrt
import colorama
import traceback
from colorama import Fore, Back, Style
import datetime


class To_do:
    unstarted   = 0
    in_progress = 1
    done        = 2
    admin       = 3
    
    regression = "REGTEST"
    misc = "MISCELLANEOUS"
    
    def __init__(self, name, level=0): #0 = .unstarted
        self.name = name
        self.level = level
        
    def __str__(self):
        return self.name + "," + str(self.level)
        
    def progress(self):
        if (self.level != To_do.admin):
            self.level += 1
            self.name = "    " + self.name
            if (self.level > To_do.done):
                self.level = To_do.unstarted
                self.name = self.name[12:]
            
    def progress_by_name(list, name):
        for to_do in list:
            if (to_do.name == name):
                to_do.progress()
                
    def set_admin(self):
        self.level = To_do.admin
            

class To_do_menu(JU.Menu):

    def __init__(self, to_do_list):
    
        self.menuItems = []
        self.unselected = Back.WHITE + Fore.BLUE + Style.NORMAL
        self.selected = Fore.CYAN + Style.BRIGHT
        self.unstarted = Fore.RED + Style.BRIGHT
        self.in_progress = Fore.YELLOW + Style.BRIGHT
        self.done = Fore.GREEN + Style.NORMAL
        self.header = ""
        self.currSelection = 0
        self.scrollWindowSize = (20 - 1) #written this way because index from 0
        self.endScroll = 0
        self.scrollWindowTop = 0
        self.scrollWindowBottom = self.scrollWindowSize
        counter = 0
  
        for to_do in to_do_list:
            if(to_do.name[0:3] == "***"):
                self.endScroll = counter
            else:
                self.menuItems.append(to_do) 
                counter += 1
                
        while(self.option(self.currSelection) == ""):
            self.currSelection += 1
    
    def getLevel(self, index):
        return self.menuItems[index].level
        
    def option(self,index):
        return self.menuItems[index].name
        
    def run(self):
        self.update()
        keepRunning = True
        while(keepRunning):
            key = JU.Kbd.getKey()

            if (key == JU.Kbd.UP):

                while(True):
                    self.currSelection -= 1
                    if (self.currSelection < 0):
                        self.currSelection = len(self.menuItems) - 1
                    if (self.option(self.currSelection) != ""):
                        break
                self.update()

            if (key == JU.Kbd.DOWN):
                while(True):
                    self.currSelection += 1
                    if (self.currSelection > (len(self.menuItems) - 1)):
                        self.currSelection = 0
                    if (self.option(self.currSelection) != ""):
                        break    
                self.update()

            if (key == JU.Kbd.RIGHT):
                self.currSelection = len(self.menuItems) - 1
                self.update()

            if (key == JU.Kbd.LEFT):
                self.currSelection = 0
                self.update()

            if (key == JU.Kbd.ENTER):
                keepRunning = False    
                
        self.execute()        
        
        return self.option(self.currSelection)
        
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
                print(self.selected + self.option(index))
            elif (self.getLevel(index) == To_do.admin):
                print(self.unselected + self.option(index))		
            elif (self.getLevel(index) == To_do.unstarted): 
                print(self.unstarted + self.option(index))				
            elif (self.getLevel(index) == To_do.in_progress): 
                print(self.in_progress + self.option(index))
            elif (self.getLevel(index) == To_do.done): 
                print(self.done + self.option(index))            
    
    def execute(self):
        print(self.unselected)
        os.system('cls')
        
           
def import_save_file(file_path, list_type):
    valid_type = False
    if (list_type == To_do.regression):
        tag = To_do.regression
        index = 0
        valid_type = True
    elif (list_type == To_do.misc):
        tag = To_do.misc
        index = 1
        valid_type = True

    if (valid_type):
        with open(file_path, "r") as f:
            lines = f.readlines()
        to_dos = []
        new_list = []

        for line in lines:
            new_line = line.rstrip("\n")
            new_line = new_line.split(",")
            to_dos.append(new_line)

        for to_do in to_dos:
            if (to_do[0] == tag):
                for i in range(len(to_do) // 2):
                    new_to_do = To_do(to_do[2*i+1], int(to_do[2*i+2]))
                    new_list.append(new_to_do)
    return new_list
                
def export_save_file(file_path, to_do_list, list_type):
    valid_type = False
    if (list_type == To_do.regression):
        tag = To_do.regression
        index = 0
        valid_type = True
    elif (list_type == To_do.misc):
        tag = To_do.misc
        index = 1
        valid_type = True

    if (valid_type):
        with open(file_path, "r") as file:
            text = file.readlines()
        with open(file_path, "w") as file:
            output_line = tag
            for item in to_do_list:
                if(item.level != To_do.admin):
                    output_line += ","
                    output_line += item.name
                    output_line += ","
                    output_line += str(item.level)
            text[index] = output_line + "\n"
            file.write(''.join(text))
            
class Menu_handler:            

    def __init__(self, save_file, tag):
        self.menu = None
        self.test_list = []
        self.tag = tag
        self.save_file = save_file

    def add_new_batch(self):
        fw_title = input("What Firmware Version Are You Testing?:\n >>> ")
        
        self.menu.menuItems.insert(-4, To_do(fw_title.upper() + " LPO 8G SLC"))
        self.menu.menuItems.insert(-4, To_do(fw_title.upper() + " LPO 480G MLC"))
        self.menu.menuItems.insert(-4, To_do(fw_title.upper() + " fsync 8G SLC"))
        self.menu.menuItems.insert(-4, To_do(fw_title.upper() + " fsync 50G 4PL"))
        self.menu.menuItems.insert(-4, To_do(fw_title.upper() + " fsync 100G 4PL"))
        self.menu.menuItems.insert(-4, To_do(fw_title.upper() + " fsync 200G MLC"))
        
    def clear_admin_tests (self):
        accumulator_list = []
        for to_do in self.test_list:
            if (to_do.level != To_do.admin):
                accumulator_list.append(to_do)
        self.test_list = accumulator_list
    
    def clear_finished_tests(self):
        working_tests = []
        for test in self.test_list:
            if(test.level != To_do.done):
                working_tests.append(test)
        self.test_list = working_tests
        
    def open_menu(self):
                
        self.test_list = import_save_file(self.save_file, self.tag)
        
        add_batch = "Add New Regression Test"
        clear_finished = "Clear Finished Tests"
        quit = "Quit"
        
        self.test_list.append(To_do("",To_do.admin))
        self.test_list.append(To_do(add_batch,To_do.admin))
        self.test_list.append(To_do(clear_finished, To_do.admin))
        self.test_list.append(To_do(quit,To_do.admin))
        self.menu = To_do_menu(self.test_list)
        
        while(True):
            selected_option = self.menu.run()
            
            if(selected_option == add_batch):
                self.add_new_batch()
                self.menu.currSelection = 1
            elif(selected_option == clear_finished):
                self.clear_finished_tests()
                self.menu = To_do_menu(self.test_list)
            elif(selected_option == quit):
                break
            else:
                To_do.progress_by_name(self.menu.menuItems, selected_option)
        
        self.test_list = self.menu.menuItems
        self.clear_admin_tests()
        export_save_file(self.save_file, self.test_list, self.tag)
    
class Misc_menu_handler(Menu_handler):
    
    def add_new_batch(self):
        task_title = input("What task would you like to track?:\n >>> ")
        
        self.menu.menuItems.insert(-4, To_do(task_title.upper()))
    
    def open_menu(self):
                
        self.test_list = import_save_file(self.save_file, self.tag)
        
        add_task = "Add New Task"
        clear_finished = "Clear Finished Tests"
        quit = "Quit"
        
        self.test_list.append(To_do("",To_do.admin))
        self.test_list.append(To_do(add_task,To_do.admin))
        self.test_list.append(To_do(clear_finished, To_do.admin))
        self.test_list.append(To_do(quit,To_do.admin))
        self.menu = To_do_menu(self.test_list)
        
        while(True):
            selected_option = self.menu.run()
            
            if(selected_option == add_task):
                self.add_new_batch()
                self.menu.currSelection = 1
            elif(selected_option == clear_finished):
                self.clear_finished_tests()
                self.menu = To_do_menu(self.test_list)
            elif(selected_option == quit):
                break
            else:
                To_do.progress_by_name(self.menu.menuItems, selected_option)
                
        self.test_list = self.menu.menuItems
        self.clear_admin_tests()
        export_save_file(self.save_file, self.test_list, self.tag)

    
def main():
    regression_test_list = []
    JU.initialize()
    
    save_file_path = "C:\\py\\ToDo\\SaveToDo.txt"
    
    regression_testing = "Regression Tests"
    misc_tasks         = "Miscellaneous Tasks"
    quit               = "Quit"
    
    main_menu_titles = [regression_testing, misc_tasks, quit]
    mainMenu = JU.Menu(main_menu_titles)
    mainMenu.setHeader("\n   TO DO   \n")
    
    reg_menu_handler = Menu_handler(save_file_path, To_do.regression)
    misc_menu_handler = Misc_menu_handler(save_file_path, To_do.misc)
    while (True):    
        selected_option = mainMenu.run()
        
        if (selected_option == regression_testing):
            reg_menu_handler.open_menu()            
        if (selected_option == misc_tasks):
            misc_menu_handler.open_menu()
        if (selected_option == quit):
            break
    
if (__name__ == "__main__"):
    main()