from statistics import median, mean
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import sys
import JUtil as JU
import pathlib
from tkinter import filedialog, messagebox
import tkinter.ttk
import datetime

class Drive_Latencies():

    def __init__(self, title=""):
        
        self.title = title
        self.transfers = ()
        self.latencies = ()
        self.min = 0
        self.max = 0
        self.mean = 0
        self.median = 0
        self.total_min = 0
        
    def populate(self, title=None, dialog=None):
    
        if(not dialog):
            dialog = "Choose your file for " + self.title
            
        root = tkinter.Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title=dialog,
                                                   filetypes=(('text files', '*.txt'), ('all files', '*.*')))
        # if we don't get a filename just bail
        if root.filename:
            filename = root.filename
        else:
            exit(0)
            
        with open(filename, "r") as f:
            text = f.readlines()

        transfer = 1
        for line in text:
            if ("ns" in line):
                data = re.search("^.* = ([0-9]+) s, ([0-9]+) ns$", line)
                if (data):
                    self.transfers += (transfer,)
                    transfer += 1
                    seconds = float(data.group(1).strip())
                    nanoseconds = float(data.group(2).strip())
                    miliseconds = (seconds * 1000) + (nanoseconds / 1000000)
                    self.latencies += (miliseconds,)
        
        self.min = min(self.latencies)
        self.max = max(self.latencies)
        self.mean = mean(self.latencies)
        self.median = median(self.latencies)
        self.total_min = sum(self.latencies) / (1000 * 60)
        
        if(title):
            self.title = title
            
    def get_summary(self):
        summary = ""
        summary += self.title + "\n"
        summary += "MAX   : " + str(round(self.max, 3)) + "ms\n"
        summary += "MEAN  : " + str(round(self.mean, 3)) + "ms\n"
        summary += "MEDIAN: " + str(round(self.median, 3)) + "ms\n"
        summary += "MIN   : " + str(round(self.min, 3)) + "ms\n"
        summary += "Test took " + str(round(self.total_min, 3)) + " minutes to complete " 
        summary += str(len(self.latencies)) + " 16MB transfers\n\n"
        return summary
            
class Chart_Styler():

    def __init__(self):
        self.colors = ["b", "g", "r", "k", "c", "m", "y"]
        self.styles = [".", "*", ","]
        self.count = 0
        
    def next(self):
        i_color = self.count % len(self.colors)
        i_style = self.count // len(self.colors) % len(self.styles)
        color = self.colors[i_color]
        style = self.styles[i_style]
        self.count += 1
        style = style + color
        return style
            
def main():
    now = datetime.datetime.now()
    drives = []
    charts = []
    styles = Chart_Styler()
    legend_points = ()
    legend_names = ()
    
    print("Processing trigger_fsync tests for Regression Testing:\n")
    fw_version = input("What version of FW are you testing?\n    >>> ")
    standard_EN = input("Is this a standard SM2246EN Regression Test?\n    >>> ")
    
    standard_EN = standard_EN[0].upper()
    
    if (standard_EN == "Y"):
    
        drive_8G = Drive_Latencies(title=(fw_version + " 8GB   SLC  0%WLE"))
        drives.append(drive_8G)
        
        drive_50G = Drive_Latencies(title=(fw_version + " 50GB  4PL 50%WLE"))
        drives.append(drive_50G)
        
        drive_100G = Drive_Latencies(title=(fw_version + " 100GB 4PL 50%WLE"))
        drives.append(drive_100G)
        
        drive_200G = Drive_Latencies(title=(fw_version + " 200GB MLC  0%WLE"))
        drives.append(drive_200G)
        
    else:
        num_drives = input("How many drives would you like to process?\n>>> ")
        int_received = False
        while(not int_received):
            try:
                num_drives = int(num_drives)
                int_received = True
            except ValueError:
                print("ERROR: You must enter an integer")
                num_drives = input("How many drives would you like to process?\n>>> ")
        if (num_drives <= 0):
            print("Invalid number of drives\n")
            exit(0)
        else:
            print("\nInitializing Drives:\n")
            for i in range(num_drives):
                print("\nDrive #" + str(i))
                capacity = input("    What size was the drive in GB?\n    >>> ")
                flash = input("    What type of flash was on the drive?\n    >>> ")
                wle = input("    What write latency enhancement was used on the drive?\n    >>> ")
                
                title = fw_version + " " + capacity + "GB " + flash + " " + wle + "_WLE"
                drive = Drive_Latencies(title)
                drives.append(drive)
        
    for drive in drives:
        drive.populate()
        
    filename = "C:\\py\\fsync\\fsync_" + fw_version + "_" + str(now.date())
    
    with open(filename + ".txt", "w") as outfile:
        for drive in drives:
            outfile.write(drive.get_summary())
        
    print("Summary saved to: <" + filename + ".txt>")
    
    for drive in drives:
        chart = plt.plot(drive.transfers, drive.latencies, styles.next())
        charts.append(chart)
        legend_names += (drive.title,)
        legend_points += (chart[0],)
    
    plt.ylabel("16MB Transfer Latency [ms]")
    plt.xlabel("Transfer Number")
    plt.title(fw_version + " fsync test")
    plt.xticks(np.arange(0,40000, 8000))
    plt.legend(legend_points, legend_names)
    plt.savefig(filename + ".png", dpi=1000, bbox_inches='tight', pad_inches=0.25)
    plt.clf()
    print("Chart Saved to <" + filename + ".png> in C:\\py\\fsync")        
        
if(__name__ == "__main__"):
    main()