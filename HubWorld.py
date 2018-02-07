"""When run as main, opens up the main menu of all my python projects
"""

import JUtil as JU
import subprocess as sub
import sys
import colorama
import datetime


def main():
    JU.initialize()

    run_notes_keeper = "NotesKeeper"
    run_to_do = "To Do List"
    parse_LPO = "Parse Long Power On Data"
    process_LPO = "Process Long Power On Data"
    process_CDM = "Process CDM Benchmarking Data"
    chart_CDM = "Chart CDM Benchmarking Data"
    nvme_waf = "Process E8 WAF"
    nvme_sample = "Get MP Database info from IDFY command"
    fsync = "Chart fsync "
    quit = "Quit"

    main_menu_titles = [run_notes_keeper, run_to_do, parse_LPO,
                        process_LPO, process_CDM, chart_CDM, nvme_waf,
                        nvme_sample, fsync, "", quit]

    main_menu = JU.Menu(main_menu_titles)

    while (True):
        time = datetime.datetime.today()
        main_menu.setHeader("Hub: " + JU.datetime_to_str_until_minute() + "\n")
        selectedOption = main_menu.run()

        if (selectedOption == run_notes_keeper):
            sub.call([sys.executable, "C:\\py\\NotesKeeper.py", "--debug", "--quick"])
        if (selectedOption == run_to_do):
            sub.call([sys.executable, "C:\\py\\ToDo.py"])
        if (selectedOption == parse_LPO):
            sub.call([sys.executable, "C:\\py\\ParseLongPowerOn.py", "-v"])
        if (selectedOption == process_LPO):
            sub.call([sys.executable, "C:\\py\\ProcessLongPowerOn.py"])
        if (selectedOption == process_CDM):
            sub.call([sys.executable, "C:\\py\\Process_CDM.py"])
            JU.wait()
        if (selectedOption == chart_CDM):
            sub.call([sys.executable, "C:\\py\\Process_CDM.py", "-c"])
            JU.wait()
        if (selectedOption == nvme_waf):
            sub.call([sys.executable, "C:\\py\\NVMe_WAF.py"])
            JU.wait()
        if (selectedOption == nvme_sample):
            sub.call([sys.executable, "C:\\py\\Get_Sample_Info.py"])
            JU.wait()
        if (selectedOption == fsync):
            sub.call([sys.executable, "C:\\py\\fsync_parser.py"])
            JU.wait()
        if (selectedOption == quit):
            break


if __name__ == "__main__":
    main()
