import random
from tkinter import filedialog, messagebox
import tkinter.ttk
import argparse
import os
import re
import sys
import JUtil as JU
import pathlib
import numpy as np
import matplotlib.pyplot as plt


class CDM_series:

    def __init__(self, drivedata_list=None):
        # for CDM 5 by default
        self.enable_dict = {"seq_read": False, "seq_write": False,
                            "seq_read_QD_32": True, "seq_write_QD_32": True,
                            "rand_read_512": False, "rand_write_512": False,
                            "rand_read_4k_QD_1": False, "rand_read_4k_QD_1_IOPS": False,
                            "rand_write_4k_QD_1": False, "rand_write_4k_QD_1_IOPS": False,
                            "rand_read_4k_QD_32": True, "rand_read_4k_QD_32_IOPS": False,
                            "rand_write_4k_QD_32": True, "rand_write_4k_QD_32_IOPS": False}

        if (drivedata_list is None):
            self.title = ""
            self.points = []

        else:
            self.title = drivedata_list[0].description
            self.points = find_averages(drivedata_list)
            if (int(drivedata_list[0].cdm_version) == 3):
                self.enable_dict = {"seq_read": True, "seq_write": True,
                                    "seq_read_QD_32": False, "seq_write_QD_32": False,
                                    "rand_read_512": False, "rand_write_512": False,
                                    "rand_read_4k_QD_1": False, "rand_read_4k_QD_1_IOPS": False,
                                    "rand_write_4k_QD_1": False, "rand_write_4k_QD_1_IOPS": False,
                                    "rand_read_4k_QD_32": True, "rand_read_4k_QD_32_IOPS": False,
                                    "rand_write_4k_QD_32": True, "rand_write_4k_QD_32_IOPS": False}

    def generate_chart(self):
        tick = 0
        ticks = ()
        tick_labels = ()
        data_x = ()
        data_y = ()
        averages_x = ()
        averages_y = ()

        for key in self.enable_dict:
            if (self.enable_dict[key]):
                tick += 1
                ticks += (tick,)
                tick_labels += (DriveData.return_chart_header_by_name(key),)
                for drive_data in self.points:
                    if (drive_data.run_number != "AVERAGE"):
                        data_x += (tick,)
                        data_y += (float(drive_data.return_variable_by_name(key)),)
                    else:
                        averages_x += (tick,)
                        averages_y += (drive_data.return_variable_by_name(key),)
        raw = plt.plot(data_x, data_y, '_b')
        avg = plt.plot(averages_x, averages_y, '.r')

        plt.ylabel("Drive Performance [MBps]")
        plt.xlabel("CDM Access Type")
        plt.title(self.title + " CDM Performance")
        plt.xticks(ticks, tick_labels)
        plt.yticks(np.arange(0, 2500, 500))
        plt.legend((raw[0], avg[0]), ("Raw Data", "Average"))
        print("Chart Saved to <" + self.title + "_CDM_Chart.png> in C:\py\CDM_Charts")
        plt.savefig("C:\\py\\CDM_Charts\\" + self.title + "_CDM_Chart.png", dpi=500, bbox_inches='tight',
                    pad_inches=0.25)
        plt.clf()


class DriveData:
    """Class used to hold drive performance data and return the data in csv format
    """

    def __init__(self):
        self.description = 0
        self.run_number = 0
        self.cdm_version = 0
        self.seq_read = 0
        self.seq_write = 0
        self.seq_read_QD_32 = 0
        self.seq_write_QD_32 = 0
        self.rand_read_512 = 0
        self.rand_write_512 = 0
        self.rand_read_4k_QD_1 = 0
        self.rand_read_4k_QD_1_IOPS = 0
        self.rand_write_4k_QD_1 = 0
        self.rand_write_4k_QD_1_IOPS = 0
        self.rand_read_4k_QD_32 = 0
        self.rand_read_4k_QD_32_IOPS = 0
        self.rand_write_4k_QD_32 = 0
        self.rand_write_4k_QD_32_IOPS = 0

    def __str__(self):
        """Return the members of the DriveData class in order for csv printing
        :returns string: string representation of a DriveData object
        """
        return str(self.description) + ',' + str(self.run_number) + ',' + str(self.cdm_version) + ',' + \
               str(self.seq_read) + ',' + str(self.seq_write) + ',' + \
               str(self.seq_read_QD_32) + ',' + str(self.seq_write_QD_32) + ',' + \
               str(self.rand_read_512) + ',' + str(self.rand_write_512) + ',' + \
               str(self.rand_read_4k_QD_1) + ',' + str(self.rand_read_4k_QD_1_IOPS) + ',' + \
               str(self.rand_write_4k_QD_1) + ',' + str(self.rand_write_4k_QD_1_IOPS) + ',' + \
               str(self.rand_read_4k_QD_32) + ',' + str(self.rand_read_4k_QD_32_IOPS) + ',' + \
               str(self.rand_write_4k_QD_32) + ',' + str(self.rand_write_4k_QD_32_IOPS) + '\n'

    @staticmethod
    def print_header_labels():
        """Static method to return the header record for a drive data csv file
        :returns string: header record for the csv file
        """
        return 'Drive,Run Number,CDM Version,Sequential Read,Sequential Write,' + \
               'Sequential Read (QD=32),Sequential Write (QD=32),' + \
               'Random Read 512KB,Random Write 512KB,' + \
               'Random Read 4KB (QD=1),Random Read 4KB (QD=1) IOPS,Random Write 4KB (QD=1),' + \
               'Random Write 4KB (QD=1) IOPS,Random Read 4KB (QD=32),Random Read 4KB (QD=32) IOPS,' + \
               'Random Write 4KB (QD=32),Random Write 4KB (QD=32) IOPS\n'

    @staticmethod
    def return_chart_header_by_name(name):
        chart_header = ""
        if (name == "seq_read"):
            chart_header = "Seq Read"
        elif (name == "seq_write"):
            chart_header = "Seq Write"
        elif (name == "seq_read_QD_32"):
            chart_header = "Seq Read\n\nQD = 32"
        elif (name == "seq_write_QD_32"):
            chart_header = "Seq Write\n\nQD = 32"
        elif (name == "rand_read_512"):
            chart_header = "Rand Read\n512KB"
        elif (name == "rand_write_512"):
            chart_header = "Rand Write\n512KB"
        elif (name == "rand_read_4k_QD_1"):
            chart_header = "Rand Read\n4KB\nQD = 1"
        elif (name == "rand_read_4k_QD_1_IOPS"):
            chart_header = "Rand Read\n4KB\nQD = 1\nIOPS"
        elif (name == "rand_write_4k_QD_1"):
            chart_header = "Rand Write\n4KB\nQD = 1"
        elif (name == "rand_write_4k_QD_1_IOPS"):
            chart_header = "Rand Write\n4KB\nQD = 1\nIOPS"
        elif (name == "rand_read_4k_QD_32"):
            chart_header = "Rand Read\n4KB\nQD = 32"
        elif (name == "rand_read_4k_QD_32_IOPS"):
            chart_header = "Rand Read\n4KB\nQD = 32\nIOPS"
        elif (name == "rand_write_4k_QD_32"):
            chart_header = "Rand Write\n4KB\nQD = 32"
        elif (name == "rand_write_4k_QD_32_IOPS"):
            chart_header = "Rand Write\n4KB\nQD = 32\nIOPS"
        else:
            chart_header = "INVALID NAME"
        return chart_header

    # noinspection PyMethodMayBeStatic
    def return_variable_by_name(self, name):
        variable_by_name = 0
        command = "self." + name
        variable_by_name = eval(command)
        return variable_by_name


def read_file(file_name, verbose=True):
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


def build_drive_list(text, verbose=False):
    """Build a list of DriveData objects from the input file. Optional verbosity param
    :param text: list of lines from the input file
    :param verbose: run with extra logging
    :returns total_results: list of DriveData objects
    """
    drive_active = False
    first_record = True
    total_results = []
    for line in text:
        if not drive_active or first_record:
            drive = DriveData()
            first_record = False
        if 'Run' in line:
            drive_active = True
            data = re.search('(^.*GB?) (.*)[Rr]un(.\d)', line)
            if data:
                drive.description = data.group(1).strip() + ' ' + data.group(2).strip()
                drive.run_number = data.group(3).strip()
                continue
        elif 'CrystalDiskMark' in line and drive_active:
            data = re.search('CrystalDiskMark ([35])', line)
            if data:
                drive.cdm_version = data.group(1).strip()
                continue
        if (drive.cdm_version == 0):
            # Do nothing
            continue
        elif (str(drive.cdm_version) == "3"):
            if 'Sequential Read :' in line and drive_active:
                data = re.search('Sequential Read : (.*) MB/s', line)
                if data:
                    drive.seq_read = data.group(1).strip()
                    continue
            elif 'Sequential Write :' in line and drive_active:
                data = re.search('Sequential Write : (.*) MB/s', line)
                if data:
                    drive.seq_write = data.group(1).strip()
                    continue
            elif 'Random Read 512KB' in line and drive_active:
                data = re.search('Random Read 512KB : (.*) MB/s', line)
                if data:
                    drive.rand_read_512 = data.group(1).strip()
                    continue
            elif 'Random Write 512KB' in line and drive_active:
                data = re.search('Random Write 512KB : (.*) MB/s', line)
                if data:
                    drive.rand_write_512 = data.group(1).strip()
                    continue
            elif 'Random Read 4KB (QD=1)' in line and drive_active:
                data = re.search('Random Read 4KB \(QD=1\) : (.*) MB/s.*\[(.*)IOPS\]', line)
                if data:
                    drive.rand_read_4k_QD_1 = data.group(1).strip()
                    drive.rand_read_4k_QD_1_IOPS = data.group(2).strip()
                    continue
            elif 'Random Write 4KB (QD=1)' in line and drive_active:
                data = re.search('Random Write 4KB \(QD=1\) : (.*) MB/s.*\[(.*)IOPS\]', line)
                if data:
                    drive.rand_write_4k_QD_1 = data.group(1).strip()
                    drive.rand_write_4k_QD_1_IOPS = data.group(2).strip()
                    continue
            elif 'Random Read 4KB (QD=32)' in line and drive_active:
                data = re.search('Random Read 4KB \(QD=32\) : (.*) MB/s.*\[(.*)IOPS\]', line)
                if data:
                    drive.rand_read_4k_QD_32 = data.group(1).strip()
                    drive.rand_read_4k_QD_32_IOPS = data.group(2).strip()
                    continue
            elif 'Random Write 4KB (QD=32)' in line and drive_active:
                data = re.search('Random Write 4KB \(QD=32\) : (.*) MB/s.*\[(.*)IOPS\]', line)
                if data:
                    drive.rand_write_4k_QD_32 = data.group(1).strip()
                    drive.rand_write_4k_QD_32_IOPS = data.group(2).strip()
                    # this should be the last record, so set drive_active to False and store it in the total_result list
                total_results.append(drive)
                drive_active = False
        elif (str(drive.cdm_version) == "5"):
            if 'Sequential Read (Q= 32,T=' in line and drive_active:
                data = re.search('Sequential Read \(Q= 32,T= [0-9]*\) : (.*) MB/s', line)
                if data:
                    drive.seq_read_QD_32 = data.group(1).strip()
                    continue
            elif 'Sequential Write (Q= 32,T=' in line and drive_active:
                data = re.search('Sequential Write \(Q= 32,T= [0-9]*\) : (.*) MB/s', line)
                if data:
                    drive.seq_write_QD_32 = data.group(1).strip()
                    continue
            elif 'Random Read 4KiB (Q= 32,T=' in line and drive_active:
                data = re.search('Random Read 4KiB \(Q= 32,T= [0-9]*\) : (.*) MB/s.*\[(.*)IOPS\]', line)
                if data:
                    drive.rand_read_4k_QD_32 = data.group(1).strip()
                    drive.rand_read_4k_QD_32_IOPS = data.group(2).strip()
                    continue
            elif 'Random Write 4KiB (Q= 32,T=' in line and drive_active:
                data = re.search('Random Write 4KiB \(Q= 32,T= [0-9]*\) : (.*) MB/s.*\[(.*)IOPS\]', line)
                if data:
                    drive.rand_write_4k_QD_32 = data.group(1).strip()
                    drive.rand_write_4k_QD_32_IOPS = data.group(2).strip()
                    continue
            elif 'Sequential Read (T=' in line and drive_active:
                data = re.search('Sequential Read \(T= [0-9]*\) : (.*) MB/s', line)
                if data:
                    drive.seq_read = data.group(1).strip()
                    continue
            elif 'Sequential Write (T=' in line and drive_active:
                data = re.search('Sequential Write \(T= [0-9]*\) : (.*) MB/s', line)
                if data:
                    drive.seq_write = data.group(1).strip()
                    continue
            elif 'Random Read 4KiB (Q= 1,T=' in line and drive_active:
                data = re.search('Random Read 4KiB \(Q= 1,T= [0-9]*\) : (.*) MB/s.*\[(.*)IOPS\]', line)
                if data:
                    drive.rand_read_4k_QD_1 = data.group(1).strip()
                    drive.rand_read_4k_QD_1_IOPS = data.group(2).strip()
                    continue
            elif 'Random Write 4KiB (Q= 1,T=' in line and drive_active:
                data = re.search('Random Write 4KiB \(Q= 1,T= [0-9]*\) : (.*) MB/s.*\[(.*)IOPS\]', line)
                if data:
                    drive.rand_write_4k_QD_1 = data.group(1).strip()
                    drive.rand_write_4k_QD_1_IOPS = data.group(2).strip()
                    # this should be the last record, so set drive_active to False and store it in the total_result list
                    total_results.append(drive)
                    drive_active = False

    if verbose:
        print('Number of tests aggregated: <' + str(len(total_results)) + '>')

    return total_results


def find_averages(drive_list):
    averages_list = []
    current_desc = drive_list[0].description
    count = 0
    cdm_version = 0
    seq_read = 0
    seq_write = 0
    seq_read_QD_32 = 0
    seq_write_QD_32 = 0
    rand_read_512 = 0
    rand_write_512 = 0
    rand_read_4k_QD_1 = 0
    rand_read_4k_QD_1_IOPS = 0
    rand_write_4k_QD_1 = 0
    rand_write_4k_QD_1_IOPS = 0
    rand_read_4k_QD_32 = 0
    rand_read_4k_QD_32_IOPS = 0
    rand_write_4k_QD_32 = 0
    rand_write_4k_QD_32_IOPS = 0

    for drive in drive_list:
        if (drive.description == current_desc):
            cdm_version += int(drive.cdm_version)
            seq_read += float(drive.seq_read)
            seq_write += float(drive.seq_write)
            seq_read_QD_32 += float(drive.seq_read_QD_32)
            seq_write_QD_32 += float(drive.seq_write_QD_32)
            rand_read_512 += float(drive.rand_read_512)
            rand_write_512 += float(drive.rand_write_512)
            rand_read_4k_QD_1 += float(drive.rand_read_4k_QD_1)
            rand_read_4k_QD_1_IOPS += float(drive.rand_read_4k_QD_1_IOPS)
            rand_write_4k_QD_1 += float(drive.rand_write_4k_QD_1)
            rand_write_4k_QD_1_IOPS += float(drive.rand_write_4k_QD_1_IOPS)
            rand_read_4k_QD_32 += float(drive.rand_read_4k_QD_32)
            rand_read_4k_QD_32_IOPS += float(drive.rand_read_4k_QD_32_IOPS)
            rand_write_4k_QD_32 += float(drive.rand_write_4k_QD_32)
            rand_write_4k_QD_32_IOPS += float(drive.rand_write_4k_QD_32_IOPS)
            count += 1
        else:
            new_drive = DriveData()
            new_drive.description = current_desc
            new_drive.run_number = "AVERAGE"
            new_drive.cdm_version = cdm_version / count
            new_drive.seq_read = seq_read / count
            new_drive.seq_write = seq_write / count
            new_drive.seq_read_QD_32 = seq_read_QD_32 / count
            new_drive.seq_write_QD_32 = seq_write_QD_32 / count
            new_drive.rand_read_512 = rand_read_512 / count
            new_drive.rand_write_512 = rand_write_512 / count
            new_drive.rand_read_4k_QD_1 = rand_read_4k_QD_1 / count
            new_drive.rand_read_4k_QD_1_IOPS = rand_read_4k_QD_1_IOPS / count
            new_drive.rand_write_4k_QD_1 = rand_write_4k_QD_1 / count
            new_drive.rand_write_4k_QD_1_IOPS = rand_write_4k_QD_1_IOPS / count
            new_drive.rand_read_4k_QD_32 = rand_read_4k_QD_32 / count
            new_drive.rand_read_4k_QD_32_IOPS = rand_read_4k_QD_32_IOPS / count
            new_drive.rand_write_4k_QD_32 = rand_write_4k_QD_32 / count
            new_drive.rand_write_4k_QD_32_IOPS = rand_write_4k_QD_32_IOPS / count

            averages_list.append(new_drive)

            current_desc = drive.description
            cdm_version = int(drive.cdm_version)
            seq_read = float(drive.seq_read)
            seq_write = float(drive.seq_write)
            seq_read_QD_32 = float(drive.seq_read_QD_32)
            seq_write_QD_32 = float(drive.seq_write_QD_32)
            rand_read_512 = float(drive.rand_read_512)
            rand_write_512 = float(drive.rand_write_512)
            rand_read_4k_QD_1 = float(drive.rand_read_4k_QD_1)
            rand_read_4k_QD_1_IOPS = float(drive.rand_read_4k_QD_1_IOPS)
            rand_write_4k_QD_1 = float(drive.rand_write_4k_QD_1)
            rand_write_4k_QD_1_IOPS = float(drive.rand_write_4k_QD_1_IOPS)
            rand_read_4k_QD_32 = float(drive.rand_read_4k_QD_32)
            rand_read_4k_QD_32_IOPS = float(drive.rand_read_4k_QD_32_IOPS)
            rand_write_4k_QD_32 = float(drive.rand_write_4k_QD_32)
            rand_write_4k_QD_32_IOPS = float(drive.rand_write_4k_QD_32_IOPS)
            count = 1

    new_drive = DriveData()
    new_drive.description = current_desc
    new_drive.run_number = "AVERAGE"
    new_drive.cdm_version = cdm_version / count
    new_drive.seq_read = seq_read / count
    new_drive.seq_write = seq_write / count
    new_drive.seq_read_QD_32 = seq_read_QD_32 / count
    new_drive.seq_write_QD_32 = seq_write_QD_32 / count
    new_drive.rand_read_512 = rand_read_512 / count
    new_drive.rand_write_512 = rand_write_512 / count
    new_drive.rand_read_4k_QD_1 = rand_read_4k_QD_1 / count
    new_drive.rand_read_4k_QD_1_IOPS = rand_read_4k_QD_1_IOPS / count
    new_drive.rand_write_4k_QD_1 = rand_write_4k_QD_1 / count
    new_drive.rand_write_4k_QD_1_IOPS = rand_write_4k_QD_1_IOPS / count
    new_drive.rand_read_4k_QD_32 = rand_read_4k_QD_32 / count
    new_drive.rand_read_4k_QD_32_IOPS = rand_read_4k_QD_32_IOPS / count
    new_drive.rand_write_4k_QD_32 = rand_write_4k_QD_32 / count
    new_drive.rand_write_4k_QD_32_IOPS = rand_write_4k_QD_32_IOPS / count

    averages_list.append(new_drive)

    for average in averages_list:
        drive_list.append(average)

    return drive_list


def build_csv_file(drive_list, outfile_name, verbose=True):
    """Builds a csv file from a list of Drives and saves it to the output location. Optional verbosity param
    :param drive_list: list of Drive objects
    :param outfile_name: path to the output file
    :param verbose: optional run with extra logging
    """
    needs_header = True
    output_string = None

    # sort the drive list before printing
    # first by description
    sorted_drive_list = sorted(drive_list, key=lambda drive: drive.description)
    # then by run_number
    sorted(sorted_drive_list, key=lambda drive: str(drive.run_number))

    # get averages for each drive description
    sorted_drive_list = find_averages(sorted_drive_list)

    for drive in sorted_drive_list:
        if needs_header:
            needs_header = False
            output_string = DriveData.print_header_labels()
        output_string += str(drive)

    with open(outfile_name, 'w+') as out_file:
        out_file.write(output_string)
        # out_file.write("Test Case")
    # confirmation dialog because Kristina wanted one
    messagebox.showinfo('File Saved', 'New drive performance data file saved to:\n' + outfile_name)

    if verbose:
        print('File: <' + outfile_name + '> ' + 'written to current directory.')


def display_data(drive_list):
    sorted_drive_list = sorted(drive_list, key=lambda drive: drive.description)
    sorted(sorted_drive_list, key=lambda drive: str(drive.run_number))
    same_description_list = []
    current_description = sorted_drive_list[0].description
    for drive in sorted_drive_list:
        if (drive.description == current_description):
            same_description_list.append(drive)
        else:
            cdm = CDM_series(same_description_list)
            cdm.generate_chart()
            same_description_list = [drive]
            current_description = drive.description
    cdm = CDM_series(same_description_list)
    cdm.generate_chart()


def main(argv):
    parser = argparse.ArgumentParser(description='Read an input file and save the performance data as a csv.')
    parser.add_argument('-i', '--file_name', help='Name of the input file, must be in the current working directory.',
                        dest='infile_name', required=False)
    parser.add_argument('-o', '--output_file_name', help='Name of the output file.', dest='outfile_name',
                        required=False)
    parser.add_argument('-v', '--verbose', help='Run script with increased output.', action='store_true',
                        dest='verbose', required=False)
    parser.add_argument('-c', '--chart', help='Only Produces a chart, no .csv file', action='store_true',
                        dest='just_chart', required=False)

    args = parser.parse_args()

    # we didn't get any command line args, presume we want to run in GUI mode w/ a file selector
    if not args.infile_name:
        root = tkinter.Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Choose your file',
                                                   filetypes=(('text files', '*.txt'), ('all files', '*.*')))
        # if we don't get a filename just bail
        if root.filename:
            args.infile_name = root.filename
        else:
            exit(0)

    if args.verbose:
        print('Arguments used: ' + str(args))

    text = read_file(args.infile_name, args.verbose)

    drive_list = build_drive_list(text, args.verbose)

    # auto-assign a new output file name
    if not args.outfile_name:
        match = re.search('(.*)\.', args.infile_name)
        args.outfile_name = match.group(1) + '.csv'
        count = 0
        while os.path.isfile(args.outfile_name):
            count += 1
            if args.verbose:
                print('File name already taken: <' + args.outfile_name + '>')
            args.outfile_name = match.group(1) + '_' + str(count) + '.csv'
    if (not args.just_chart):
        build_csv_file(drive_list, args.outfile_name)
    display_data(drive_list)


if __name__ == "__main__":
    main(sys.argv[1:])
