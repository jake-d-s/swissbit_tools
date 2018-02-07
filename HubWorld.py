"""When run as main, opens up the main menu of all my python projects
"""

import JUtil as Ju
import subprocess as sub
import sys


def main():
    Ju.initialize()

    run_notes_keeper = "NotesKeeper"
    run_to_do = "To Do List"
    parse_lpo = "Parse Long Power On Data"
    process_lpo = "Process Long Power On Data"
    process_cdm = "Process CDM Benchmarking Data"
    chart_cdm = "Chart CDM Benchmarking Data"
    nvme_waf = "Process E8 WAF"
    nvme_sample = "Get MP Database info from IDFY command"
    fsync = "Chart fsync "
    quit_program = "Quit"

    main_menu_titles = [run_notes_keeper, run_to_do, parse_lpo,
                        process_lpo, process_cdm, chart_cdm, nvme_waf,
                        nvme_sample, fsync, "", quit_program]

    main_menu = Ju.Menu(main_menu_titles)

    while True:
        main_menu.setHeader("Hub: " + Ju.datetime_to_str_until_minute() + "\n")
        selected_option = main_menu.run()

        if selected_option == run_notes_keeper:
            sub.call([sys.executable, "C:\\py\\NotesKeeper.py", "--debug", "--quick"])
        if selected_option == run_to_do:
            sub.call([sys.executable, "C:\\py\\ToDo.py"])
        if selected_option == parse_lpo:
            sub.call([sys.executable, "C:\\py\\ParseLongPowerOn.py", "-v"])
        if selected_option == process_lpo:
            sub.call([sys.executable, "C:\\py\\ProcessLongPowerOn.py"])
        if selected_option == process_cdm:
            sub.call([sys.executable, "C:\\py\\Process_CDM.py"])
            Ju.wait()
        if selected_option == chart_cdm:
            sub.call([sys.executable, "C:\\py\\Process_CDM.py", "-c"])
            Ju.wait()
        if selected_option == nvme_waf:
            sub.call([sys.executable, "C:\\py\\NVMe_WAF.py"])
            Ju.wait()
        if selected_option == nvme_sample:
            sub.call([sys.executable, "C:\\py\\Get_Sample_Info.py"])
            Ju.wait()
        if selected_option == fsync:
            sub.call([sys.executable, "C:\\py\\fsync_parser.py"])
            Ju.wait()
        if selected_option == quit_program:
            break


if __name__ == "__main__":
    main()
