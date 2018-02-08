from tkinter import filedialog, messagebox
import tkinter.ttk
import argparse
import os
import re
import sys

def main(argv):
    txt_files_parsed = 0
    html_files_parsed = 0

    parser = argparse.ArgumentParser(description='Read an input file and save the performance data as a csv.')
    parser.add_argument('-v', '--verbose', help='Run script with increased output.', action='store_true',
                        dest='verbose', required=False)

    args = parser.parse_args()

    root = tkinter.Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilenames(initialdir="C:\\Users\\Jake\\Desktop\\Projects\\Regression Testing",
                                                title='Choose your files', filetypes=(('all files', '*.*'),))
    # if we don't get a filename just bail
    if root.filename:
        infile_names = root.filename
    else:
        exit(0)

    if args.verbose:
        print('Arguments used: ' + str(args))

    for infile in infile_names:

        if infile[-4:] == ".txt":

            text = read_file(infile, args.verbose)

            log_list = build_log_list(text, args.verbose)

            # auto-assign a new output file name

            match = re.search('(.*)\.', infile)

            dirs = match.group(1).split("/")
            dirs[-1] = "ImportEZTool_" + dirs[-1]

            outfile_name = '/'.join(dirs) + ".txt"

            count = 0
            while os.path.isfile(outfile_name):
                count += 1
                if args.verbose:
                    print('File name already taken: <' + outfile_name + '>')

                outfile_name = '/'.join(dirs) + " " + str(count) + ".txt"

            build_csv_file(log_list, outfile_name, args.verbose)
            txt_files_parsed += 1

        elif infile[-4:] == "html":

            text = read_file(infile, args.verbose)

            cycle_list = build_cycle_list(text, args.verbose)

            # auto-assign a new output file name

            match = re.search('(.*)\.', infile)

            dirs = match.group(1).split("/")
            dirs[-1] = "ImportSFT_" + dirs[-1]

            outfile_name = '/'.join(dirs) + ".txt"

            count = 0
            while os.path.isfile(outfile_name):
                count += 1
                if args.verbose:
                    print('File name already taken: <' + outfile_name + '>')

                outfile_name = '/'.join(dirs) + " " + str(count) + ".txt"

            build_csv_file(cycle_list, outfile_name, args.verbose)
            html_files_parsed += 1

    match = re.search('(.*)\.', infile_names[0])
    dirs = match.group(1).split("/")
    dirs.pop()

    out_dir = '\\'.join(dirs)

    message_string = (str(txt_files_parsed) + " EZTool files and " +
                      str(html_files_parsed) + " SFT files were parsed.\n\nOutput located" +
                      " in " + out_dir)
    messagebox.showinfo('Files Saved', message_string)


class LogData:
    """Class used to hold log detection time data and return the data in csv format
    """

    def __init__(self):
        self.logNum = ''
        self.FWBootTime = ''
        self.pwrCycleCount = ''

    def __str__(self):
        """Return the members of the LogData class in order for csv printing
        :returns string: string representation of a LogData object
        """
        return self.logNum + ',' + self.FWBootTime + ',' + self.pwrCycleCount + '\n'

    @staticmethod
    def print_header_labels():
        """Static method to return the header record for a drive data csv file
        :returns string: header record for the csv file
        """
        return 'Log #,FWBootTime[ms],Power Cycle Count\n'


class CycleData:
    """Class used to hold cycle detection time data and return the data in csv format
    """

    def __init__(self):
        self.numCycle = ''
        self.detTime = ''

    def __str__(self):
        """Return the members of the CycleData class in order for csv printing
        :returns string: string representation of a CycleData object
        """
        return self.numCycle + ',' + self.detTime + '\n'

    @staticmethod
    def print_header_labels():
        """Static method to return the header record for a drive data csv file
        :returns string: header record for the csv file
        """
        return 'Cycle,Detect Time[ms]\n'


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


def build_log_list(text, verbose=False):
    """Build a list of LogData objects from the input file. Optional verbosity param
    :param text: list of lines from the input file
    :param verbose: run with extra logging
    :returns total_results: list of LogData objects
    """
    found_log = False
    first_record = True
    total_results = []
    for line in text:
        if not found_log or first_record:
            log = LogData()
            first_record = False
        if 'FlashLog:' in line:
            found_log = True
            data = re.search('^FlashLog:([0-9]+?)$', line)
            if data:
                log.logNum = data.group(1).strip()
                continue

        elif 'FwBootTime' in line and found_log:
            data = re.search('^FwBootTime.*?0x([0-9A-Z]+?) $', line)
            if data:
                log.FWBootTime = data.group(1).strip()
                continue

        elif 'PowerCycle Count' in line and found_log:
            data = re.search('^PowerCycle Count.*?0x([0-9A-Z]+?) $', line)
            if data:
                log.pwrCycleCount = data.group(1).strip()
                total_results.append(log)
                found_log = False

    if verbose:
        print('Number of tests aggregated: <' + str(len(total_results)) + '>')

    return total_results


def build_cycle_list(text, verbose=False):
    """Build a list of CycleData objects from the input file. Optional verbosity param
    :param text: list of lines from the input file
    :param verbose: run with extra logging
    :returns total_results: list of CycleData objects
    """
    found_cycle = False
    first_record = True
    total_results = []
    for line in text:
        if not found_cycle or first_record:
            cycle = CycleData()
            first_record = False
        if 'starting, access ' in line:
            found_cycle = True
            data = re.search('^.*?Cycle ([0-9]+?) starting, access.*?$', line)
            if data:
                cycle.numCycle = data.group(1).strip()
                continue
        elif 'Device was detected after' in line and found_cycle:
            data = re.search('^.*?Device was detected after ([0-9]+?)ms.*?$', line)
            if data:
                cycle.detTime = data.group(1).strip()
                total_results.append(cycle)
                found_cycle = False

    if verbose:
        print('Number of tests aggregated: <' + str(len(total_results)) + '>')

    return total_results


def build_csv_file(list, outfile_name, verbose=True):
    """Builds a csv file from a list of Drives and saves it to the output location. Optional verbosity param
    :param list:
    :param outfile_name: path to the output file
    :param verbose: optional run with extra logging
    """
    needs_header = True
    output_string = None

    for line in list:

        if needs_header:
            needs_header = False
            output_string = ''

        output_string += str(line)

    with open(outfile_name, 'w+') as out_file:
        out_file.write(output_string)

    # confirmation dialog because Kristina wanted one
    # messagebox.showinfo('File Saved', 'New FWBootTime log data file saved to:\n' + outfile_name)

    if verbose:
        print('File: <' + outfile_name + '> ' + 'written to current directory.')


if __name__ == "__main__":
    main(sys.argv[1:])
