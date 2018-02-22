from tkinter import filedialog
import tkinter.ttk
import JUtil as JU
import datetime

    
def get_host_writes(filename):
    text = ""
    text += "Host Writes Low  (hex): "
    low = JU.get_little_endian_from_DM_ASCII_file(filename, 48, 55, print_hex=False)
    text += low + "\n"
    text += "Host Writes High (hex): "
    high = JU.get_little_endian_from_DM_ASCII_file(filename, 56, 63, print_hex=False)
    text += high + "\n"
    total = high + low
    total = int(total, 16) * 1000 * 512
    text += "Host Writes    (Bytes): " + str(total) + "\n"
    return total, text
    
    
def get_flash_writes(filename):
    text = ""
    text += "Flash Writes     (hex): "
    total = JU.get_little_endian_from_DM_ASCII_file(filename, 328, 335, print_hex=False)
    text += total + "\n"
    total = int(total, 16) * 512
    text += "Flash Writes   (Bytes): " + str(total) + "\n"
    return total, text


def get_total_erase_count(filename):
    text = ""
    text += "Erase Count      (hex): "
    total = JU.get_little_endian_from_DM_ASCII_file(filename, 465, 472, print_hex=False)
    text += total + "\n"
    total = int(total, 16)
    text += "Erase Count   (blocks): " + str(total) + "\n"
    return total, text


def get_erase_block_size(capacity):
    capacity = int(capacity)
    mb_12 = 12 * 1024 * 1024
    size = 0
    
    # 16MB * number of CE * number of planes * MAGIC
    if capacity > 512:  # 1TB
        size = mb_12 * 32 * 2
    elif capacity > 256:  # 512GB
        size = mb_12 * 16 * 2
    elif capacity > 128:  # 256GB
        size = mb_12 * 8 * 2
    else:  # 128GB
        size = mb_12 * 4 * 2 
        
    return size


def main():

    root = tkinter.Tk()
    root.withdraw()
    waf_directory = "C:\\Users\\Jake\\Desktop\\Projects\\PCIe Controller Evaluation\\PCIe E8 WAF"
    root.filename = filedialog.askopenfilename(initialdir=waf_directory,
                                               title='Select BEFORE Test Log Page 02 (SMART)',
                                               filetypes=(('text files', '*.txt'), ('all files', '*.*')))
    # if we don't get a filename just bail
    if root.filename:
        before_SMART_file = root.filename
    else:
        exit(0)
        
    root.filename = filedialog.askopenfilename(initialdir=waf_directory,
                                               title='Select AFTER Test Log Page 02 (SMART)',
                                               filetypes=(('text files', '*.txt'), ('all files', '*.*')))
    # if we don't get a filename just bail
    if root.filename:
        after_SMART_file = root.filename
    else:
        exit(0)
        
    root.filename = filedialog.askopenfilename(initialdir=waf_directory,
                                               title='Select BEFORE Test Log Page C0 (Vendor SMART)',
                                               filetypes=(('text files', '*.txt'), ('all files', '*.*')))
    # if we don't get a filename just bail
    if root.filename:
        before_VendorSMART_file = root.filename
    else:
        exit(0)
        
    root.filename = filedialog.askopenfilename(initialdir=waf_directory,
                                               title='Select AFTER Test Log Page C0 (Vendor SMART)',
                                               filetypes=(('text files', '*.txt'), ('all files', '*.*')))
    # if we don't get a filename just bail
    if root.filename:
        after_VendorSMART_file = root.filename
    else:
        exit(0)
        
    now = datetime.datetime.now()
    now = str(now)

    capacity = input("\nWhat size was the drive in GB?\n>>> ")   
    workload = input("What workload was run on the drive?\n>>> ")
    
    pe_count = 3000
    years_rated = 3
    erase_block_size = get_erase_block_size(capacity)
    sb_MB = erase_block_size / (1024 * 1024)
    
    text = ""
    text += "Current time: " + now + "\n"
    text += capacity + "GB E8 Drive running " + workload + " workload\n"
    text += "Super Block Size = " + str(erase_block_size) + " bytes or " + str(sb_MB) + "MB / block\n"
    text += "Calculations based on a " + str(years_rated) + " year rated life "
    text += "and " + str(pe_count) + " P/E cycles\n\n"
    
    text += "SMART BEFORE\n"
    (before_host_writes, new_text) = get_host_writes(before_SMART_file)
    text += new_text
    
    text += "\nSMART AFTER\n"
    (after_host_writes, new_text) = get_host_writes(after_SMART_file)
    text += new_text
        
    text += "\nVENDOR SMART BEFORE\n"
    (before_flash_writes, new_text) = get_flash_writes(before_VendorSMART_file)
    text += new_text
    
    (before_erase_count, new_text) = get_total_erase_count(before_VendorSMART_file)
    text += new_text
    
    text += "\nVENDOR SMART AFTER\n"
    (after_flash_writes, new_text) = get_flash_writes(after_VendorSMART_file)
    text += new_text
    
    (after_erase_count, new_text) = get_total_erase_count(after_VendorSMART_file)
    text += new_text
    
    host_writes = after_host_writes - before_host_writes
    flash_writes = after_flash_writes - before_flash_writes
    erase_count = after_erase_count - before_erase_count
 
    erase_count *= erase_block_size    
    
    flash_waf = flash_writes / host_writes
    flash_TBW = int(capacity) * pe_count / (1024 * flash_waf)
    flash_DWPD = flash_TBW / (years_rated * 365.25) * (1024 / int(capacity))
    
    erase_waf = erase_count / host_writes
    erase_TBW = int(capacity) * pe_count / (1024 * erase_waf)
    erase_DWPD = erase_TBW / (years_rated * 365.25) * (1024 / int(capacity))
    
    text += "\nTOTAL SUMMARY\n"
    text += "host writes : " + str(host_writes) + " Bytes\n"
    text += "flash writes: " + str(flash_writes) + " Bytes\n"    
    text += "data erased : " + str(erase_count) + " Bytes\n\n"
    text += "   flash WAF: " + str(round(flash_waf, 3)) + "\n"
    text += "   flash TBW: " + str(round(flash_TBW, 3)) + "\n"
    text += "  flash DWPD: " + str(round(flash_DWPD, 3)) + "\n\n"
    text += "   erase WAF: " + str(round(erase_waf, 3)) + "\n"
    text += "   erase TBW: " + str(round(erase_TBW, 3)) + "\n"
    text += "  erase DWPD: " + str(round(erase_DWPD, 3)) + "\n\n"
    text += "                                                        \n"
    text += "++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    text += "                                                        \n\n"
    
    with open("C:\\py\\WAF\\WAF_logs.txt", "a") as outfile:
        outfile.write(text)
        
    print(text)


if __name__ == "__main__":
    main()
