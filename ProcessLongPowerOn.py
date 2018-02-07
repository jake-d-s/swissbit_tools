import leather
import random
from tkinter import filedialog, messagebox
import tkinter.ttk
import argparse
import os
import re
import sys
import JUtil as JU
import pathlib

class LPOSeries:

    def __init__(self, scale=1, max_time_s=20):
        self.title = "Data"
        self.scale = scale
        self.max_time_s = max_time_s
        self.sft_offset = 0
        self.ezt_offset = 0

        self.sft_cycles = []  # SFT_cycle objects
        self.ezt_cycles = []  # EZT_cycle objects

        self.cycles = []  # Power_cycle objects
        self.failed_cycles = [] # Power_cycle objects
        self.max_cycle = None # Highest Power Cycle

    def add_sft_cycle(self, new_cycle):
        duplicate_cycle = False
        for cycle in self.sft_cycles:
            if (cycle.power_cycle == new_cycle.power_cycle):
                duplicate_cycle = True
            if (cycle.power_cycle > new_cycle.power_cycle):
                break
        if (not duplicate_cycle):
            self.sft_cycles.append(new_cycle)
            self.sft_cycles.sort(key=lambda cyc: cyc.power_cycle)

    def add_ezt_cycle(self, new_cycle):
        duplicate_cycle = False
        for cycle in self.ezt_cycles:
            if (cycle.power_cycle == new_cycle.power_cycle):
                duplicate_cycle = True
            if (cycle.power_cycle > new_cycle.power_cycle):
                break
        if (not duplicate_cycle):
            self.ezt_cycles.append(new_cycle)
            self.ezt_cycles.sort(key=lambda cyc: cyc.power_cycle)

    def generate_power_cycle_list(self):
        sft_index = 0
        ezt_index = 0

        while (sft_index < len(self.sft_cycles) and 
               ezt_index < len(self.ezt_cycles)
              ):
            sft = self.sft_cycles[sft_index]
            ezt = self.ezt_cycles[ezt_index]
            if (sft.power_cycle == ezt.power_cycle):
                new_power_cycle = Power_cycle(sft.power_cycle, 
                                              ezt.ezt_cycle,
                                              sft.sft_cycle,
                                              ezt.detect_time_s,
                                              sft.detect_time_s)
                self.cycles.append(new_power_cycle)
                if (new_power_cycle.max_time() > self.max_time_s):
                    self.failed_cycles.append(new_power_cycle)
                sft_index += 1
                ezt_index += 1
            elif (sft.power_cycle > ezt.power_cycle):
                new_power_cycle = Power_cycle(ezt.power_cycle, 
                                              ezt.ezt_cycle,
                                              0,
                                              ezt.detect_time_s,
                                              0)
                self.cycles.append(new_power_cycle)
                if (new_power_cycle.max_time() > self.max_time_s):
                    self.failed_cycles.append(new_power_cycle)
                ezt_index += 1
            elif (sft.power_cycle < ezt.power_cycle):
                new_power_cycle = Power_cycle(sft.power_cycle, 
                                              0,
                                              sft.sft_cycle,
                                              0,
                                              sft.detect_time_s)
                self.cycles.append(new_power_cycle)
                if (new_power_cycle.max_time() > self.max_time_s):
                    self.failed_cycles.append(new_power_cycle)
                sft_index += 1
        if (sft_index >= len(self.sft_cycles) and
            ezt_index < len(self.ezt_cycles)):
            while (ezt_index < len(self.ezt_cycles)):
                ezt = self.ezt_cycles[ezt_index]
                new_power_cycle = Power_cycle(ezt.power_cycle, 
                                          ezt.ezt_cycle,
                                          0,
                                          ezt.detect_time_s,
                                          0)
                self.cycles.append(new_power_cycle)
                if (new_power_cycle.max_time() > self.max_time_s):
                    self.failed_cycles.append(new_power_cycle)
                ezt_index += 1
        elif (sft_index < len(self.sft_cycles) and
              ezt_index >= len(self.ezt_cycles)):
            while (sft_index < len(self.sft_cycles)):
                sft = self.sft_cycles[sft_index]
                new_power_cycle = Power_cycle(sft.power_cycle, 
                                              0,
                                              sft.sft_cycle,
                                              0,
                                              sft.detect_time_s)
                self.cycles.append(new_power_cycle)
                if (new_power_cycle.max_time() > self.max_time_s):
                    self.failed_cycles.append(new_power_cycle)
                sft_index += 1
                
        last_cycle = self.cycles[0]
        for cycle in self.cycles:
            if (cycle.sft_cycle < last_cycle.sft_cycle):
                if(not last_cycle.max_time() > self.max_time_s):
                    self.failed_cycles.append(last_cycle)
                if(not cycle.max_time() > self.max_time_s):
                    self.failed_cycles.append(cycle)
            last_cycle = cycle
        self.failed_cycles.sort(key=lambda cycle: cycle.power_cycle)

    def get_sft_points(self):
        point_list = []
        for sft in self.sft_cycles:
            point_list.append(sft.get_coords(self.sft_offset, self.scale))
        return point_list

    def get_ezt_points(self):
        point_list = []
        for ezt in self.ezt_cycles:
            point_list.append(ezt.get_coords(self.ezt_offset, self.scale))
        return point_list

    def find_max_cycle(self):
        if (len(self.cycles) > 0 ):
            self.max_cycle = self.cycles[0]
            for cycle in self.cycles:
                if (cycle.max_time() > self.max_cycle.max_time()):
                    self.max_cycle = cycle
                    
        return self.max_cycle

class SFT_cycle:

    def __init__(self, starting_cycle, current_cycle, detect_time_ms):
        self.power_cycle = JU.little_endian_str_to_int(starting_cycle) + int(current_cycle, 10)
        self.sft_cycle = int(current_cycle, 10)
        self.detect_time_s = int(detect_time_ms, 10) / 1000

    def get_coords(self, offset, scale):
        x = offset + (self.power_cycle / scale)
        y = self.detect_time_s
        return (x, y)

class EZT_cycle:

    def __init__(self, log_num, power_cycle_num_hex, det_time_ms_hex):
        self.power_cycle = int(power_cycle_num_hex, 16)
        self.ezt_cycle = int(log_num, 10)
        self.detect_time_s = int(det_time_ms_hex, 16) / 1000

    def get_coords(self, offset, scale):
        x = offset + (self.power_cycle / scale)
        y = self.detect_time_s
        return (x, y)

class Power_cycle():

    def __init__(self,
                 power_cycle,
                 ezt_cycle,
                 sft_cycle,
                 ezt_det_time,
                 sft_det_time):

        self.power_cycle = power_cycle
        self.ezt_cycle = ezt_cycle
        self.sft_cycle = sft_cycle
        self.ezt_det_time = ezt_det_time
        self.sft_det_time = sft_det_time

    @staticmethod
    def get_csv_header():
        return "Power Cycle,EZTool Log#,SFT Cycle,EZTool time [s],SFT time [s]"

    @staticmethod
    def get_display_header():
        header = (" POWER |  EZT  |  SFT  |  EZT |  SFT \n" +
                  " CYCLE | CYCLE | CYCLE | TIME | TIME \n"
                 )
        return header
        
    def max_time(self):
        if (self.ezt_det_time > self.sft_det_time):
            time = self.ezt_det_time
        else:
            time = self.sft_det_time
        return time

    def get_csv_line(self):
        str_pc = str(self.power_cycle)
        str_ezt_c = str(self.ezt_cycle)
        str_sft_c = str(self.sft_cycle)
        str_ezt_t = str(self.ezt_det_time)
        str_sft_t = str(self.sft_det_time)
        line = ','.join([str_pc, str_ezt_c, str_sft_c, str_ezt_t, str_sft_t])
        line += "\n"
        return line

    def get_display_line(self):
        str_pc = str(self.power_cycle).rjust(6) + " "
        str_ezt_c = str(self.ezt_cycle).rjust(6) + " "
        str_sft_c = str(self.sft_cycle).rjust(6) + " "
        str_ezt_t = str(round(self.ezt_det_time, 1)).rjust(5) + " "
        str_sft_t = str(round(self.sft_det_time, 1)).rjust(5) + " "
        line = '|'.join([str_pc, str_ezt_c, str_sft_c, str_ezt_t, str_sft_t])
        line += "\n"
        return line
    
def read_file(file_name, verbose=False):
    """Takes a file name and returns the lines from the file as a list. Optional verbosity param
    :param file_name: path to file to be read
    :param verbose: run with extra logging
    :returns lines: list strings representing lines in the file
    """
    if verbose:
        print('Reading file: <' + file_name + '>')

    lines = None
    with open(file_name, 'r+') as infile:
        lines = infile.readlines()

    if verbose:
        print('Lines read: <' + str(len(lines)) + '>')

    return lines        
        
def build_ezt_list(text, verbose=False):
    """Build a list of EZT_cycle objects from the input file. Optional verbosity param
    :param text: list of lines from the input file
    :param verbose: run with extra logging
    :returns total_results: list of EZT_cycle objects
    """
    total_results = []
    for line in text:         
        if 'FlashLog:' in line:
            data = re.search('^FlashLog:([0-9]+?)$', line)
            if data:
                logNum = data.group(1).strip()                
                continue
            
        elif 'FwBootTime' in line:
            data = re.search('^FwBootTime.*?0x([0-9A-Z]+?) $', line)
            if data:
                FWBootTime = data.group(1).strip()
                continue

        elif 'PowerCycle Count' in line:
            data = re.search('^PowerCycle Count.*?0x([0-9A-Z]+?) $', line)
            if data:
                pwrCycleCount = data.group(1).strip()
                new_cycle = EZT_cycle(logNum, pwrCycleCount, FWBootTime)
                total_results.append(new_cycle)
		
    if verbose:
        print('Number of tests aggregated: <' + str(len(total_results)) + '>')

    return total_results
        
def build_sft_list(text, verbose=False):
    """Build a list of SFT_cycle objects from the input file. Optional verbosity param
    :param text: list of lines from the input file
    :param verbose: run with extra logging
    :returns total_results: list of SFT_cycle objects
    """
    starting_cycle = ""
    cycle_num = ""
    det_time = ""
    total_results = []
    for line in text:
        if "Power Cycle Count<" in line:
            data = re.search('^.*?Power Cycle Count<.*?New,monospace">([0-9abcdef]*?)<', line)
            if data:
                starting_cycle = data.group(1).strip()
                continue            
        elif 'starting, access ' in line:
            data = re.search('^.*?Cycle ([0-9]+?) starting, access.*?$', line)
            if (data and starting_cycle):
                cycle_num = data.group(1).strip()        
                continue
        elif 'Device was detected after' in line:
            data = re.search('^.*?Device was detected after ([0-9]+?)ms.*?$', line)
            if (data and starting_cycle and cycle_num):
                det_time = data.group(1).strip()
                new_cycle = SFT_cycle(starting_cycle, cycle_num, det_time)
                total_results.append(new_cycle)
		
    if verbose:
        print('Number of tests aggregated: <' + str(len(total_results)) + '>')

    return total_results        

def main():
    verbose = True
    out_dir = ""

    root = tkinter.Tk()
    root.withdraw()
    
    num_drives = input("How many drives would you like to process?\n>>> ")
    int_received = False
    while(not int_received):
        try:
            num_drives = int(num_drives)
            int_received = True
        except ValueError:
            print("ERROR: You must enter an integer")
            num_drives = input("How many drives would you like to process?\n>>> ")
            
    if(num_drives <= 0):
        print("Too Few Drives")
        exit(0)
        
    lpo_drive_list = []
    
    for drive_num in range(num_drives):
        txt_files_parsed = 0
        html_files_parsed = 0
        drive_name = input("What would you like to call drive #" + str(drive_num) + "?\n>>> ")
        lpo = LPOSeries()
        lpo.title = drive_name
    
        root.filename = filedialog.askopenfilenames(initialdir=("C:\\Users\\Jake\\Desktop\\Projects\\Regression Testing"),
                                                    title=("Choose files for " + drive_name), filetypes=(('all files', '*.*'),))
        # if we don't get a filename just bail
        if root.filename:
            infile_names = root.filename
            if (out_dir == ""):
                match = re.search('(.*)\.', infile_names[0])            
                dirs = match.group(1).split("/")
                dirs.pop()               
                out_dir = '\\'.join(dirs) + "\\Processed"
                pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True) 
        else:
            exit(0)
            
        eztool_present = False
        sft_present = False
        for infile in infile_names:

            if(infile[-4:] == ".txt"):
                eztool_present = True
                text = read_file(infile, verbose)
                ezt_list = build_ezt_list(text, verbose)
                txt_files_parsed += 1
                for ezt in ezt_list:
                    lpo.add_ezt_cycle(ezt)
                
            elif(infile[-4:] == "html"):
                sft_present = True
                text = read_file(infile, verbose)
                sft_list = build_sft_list(text, verbose)
                html_files_parsed += 1
                for sft in sft_list:
                    lpo.add_sft_cycle(sft)
                    
        if (not eztool_present):
            ezt = EZT_cycle("1","1","1")
            lpo.add_ezt_cycle(ezt)
            
        if (not sft_present):
            sft = SFT_cycle("1","1","1")
        
        message_string = (str(txt_files_parsed) + " EZTool files and " + 
            str(html_files_parsed) + " SFT files were parsed for " +
            drive_name + "\n")
        if (verbose):
            print(message_string)
        lpo_drive_list.append(lpo)
    
    for lpo in lpo_drive_list:
        lpo.generate_power_cycle_list()
        
    chart_list = []
    for lpo in lpo_drive_list:
        power_cycle_file = out_dir + "\\" + lpo.title + "_AllCycles.txt"
        failing_cycle_file = out_dir + "\\" + lpo.title + "_ImportantCycles.txt"
        chart_file = out_dir + "\\" + lpo.title + "_Chart.svg"
        with open(power_cycle_file, "w") as f:
            f.write(Power_cycle.get_display_header())
            for cycle in lpo.cycles:
                f.write(cycle.get_display_line())
        with open(failing_cycle_file, "w") as f:
            f.write(Power_cycle.get_display_header())
            for cycle in lpo.failed_cycles:
                f.write(cycle.get_display_line())
        sft_data = lpo.get_sft_points()
        ezt_data = lpo.get_ezt_points()
        chart = leather.Chart(lpo.title)
        chart.add_dots(ezt_data,name="EZTool FWBootTime", radius=1.5)
        chart.add_dots(sft_data,name="SFT Detect Time", radius=1.5)
        x_axis = leather.Axis(name="Power Cycle")
        y_axis = leather.Axis(name="Detect Time in Seconds")
        chart.set_x_axis(x_axis)
        chart.set_y_axis(y_axis)
        chart.to_svg(chart_file, 500, 400)
        chart_list.append(chart)
    if (len(chart_list) > 1):
        grid_file = out_dir + "\\"
        for lpo in lpo_drive_list:
            grid_file += lpo.title + "_"
        grid_file += "_Grid.svg"
        grid = leather.Grid()
        grid.add_many(chart_list)
        grid.to_svg(grid_file, 800, 600)
        
    max_file = out_dir + "\\" + "MaxPowerOnTimes.txt"
    max_text = "Max Times per Drive:\n"
    for lpo in lpo_drive_list:
        lpo.find_max_cycle()
        max_text += lpo.title + ": " + str(round(lpo.max_cycle.max_time(), 2)) + "\n"
    with open(max_file, "w") as f:
        f.write(max_text)
    if(num_drives != 0):
        print("Processed Data stored in the directory:\n\n" + out_dir)
    else:
        print("You chose to process 0 drives, program exiting")
    JU.wait()

        
        
if __name__ == "__main__":
    main()