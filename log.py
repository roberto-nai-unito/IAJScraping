# log.py

# Log manager to tace the scaping in "01_scraper.py"

import os

log_dir = "log"
log_name = "log"
log_ext = ".txt"
file_name = ""

def log_manager(start_time, year_search):
    global log_dir
    global log_name
    global log_ext
    global file_name
    time = str(start_time).replace(":","-").replace(" ","_")
    file_name = time + "_" + log_name + "_" + str(year_search) + log_ext # example: 2023-01-15_16-57-34_log_2007.txt
    file_path = log_dir + os.sep + file_name
    fp = open(file_path, "w")
    fp.close()

def log_writer(string):
    global log_dir
    global log_name
    global log_ext
    global file_name
    file_path = log_dir + os.sep + file_name
    fp = open(file_path, mode='a')
    fp.write(string + os.linesep)
    fp.close()
