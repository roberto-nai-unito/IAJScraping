# 03_analyzer.py

# analyze the file downloaded

import os
from os import path

from datetime import datetime

import pandas as pd

import pathlib

### GLOBALS ###

sentences_dir = "sentences" # <-- input dir with all the sentences

sentences_stat_dir = "sentences_stats"

# dictionaries of the files found
court_dic = {}
year_dic = {}
ext_dic = {}

# court info
court_dir = "court"
court_file = "court.csv"

### FUNCTIONS ###

def court_load():
    """ Load the court dictionary """
    file_path = court_dir + os.sep + court_file
    df = pd.read_csv(file_path, sep = ";", header = None)
    print(df.head())
    print()
    print("DF length:", len(df))
    print()
    list_court = df[0].to_list()
    return list_court

def court_get_by_file(file, list_court):
    """ Given a file name, returns the court """
    for court in list_court:
        if file.startswith(court):
            return court
    return None

def dic_show(input_dic, title):
    """Show a dictionary"""
    sum = 0
    print("Dicionary:", title)
    print()
    for key in input_dic:
        ratio = round(input_dic[key]/total,3)
        perc = ratio * 100
        print(key,":",input_dic[key],"->",perc,"%")
        sum += input_dic[key]
    print()

    print("Sum of key values:", sum)
    print()

def dic_save(input_dic, file_name):
    """Save a dictionary to csv"""
    path_out = sentences_stat_dir + os.sep + file_name
    with open(path_out, 'w') as fp:
        fp.write('Key;Count;Perc' + os.linesep)
        for key in input_dic:
            ratio = round(input_dic[key]/total,3)
            perc = ratio * 100
            strcsv = str(key) + ";" + str(input_dic[key]) + ";" + str(perc) + os.linesep
            fp.write(strcsv)

### MAIN ###

print()
print("*** WEB SCRAPER / ANALYZER ***")

start_time = datetime.now().replace(microsecond=0)

print("Sentence directory (source):", sentences_dir)
print()

# COURT
list_court = court_load() # get the court list

year_start = 2007 # <-- INPUT
year_end = 2023 # <-- INPUT (excluded)

total = 0

for year in range(year_start, year_end):
    # year is the directory of sentences grouped by year
    dir = str(year)
    print()
    print("Sentence directory:", dir)
    print()
    path_dir = sentences_dir + os.sep + dir
    if (os.path.exists(path_dir) == True):
        i = 0
        for file in os.listdir(path_dir): # get all the files from path_dir
            if (file.startswith("._")): # avoid Mac temp files
                continue
            # get file names
            print("[",i,"] file found:", file)
            path_all = sentences_dir + os.sep + dir + os.sep + file
            extension = pathlib.Path(path_all).suffix[1:] # get extension without .
            print("Extension:", extension) 
            if extension == "htm":
                extension = "html"
            if extension == "doc":
                extension = "DOC"
            if extension == "docx":
                extension = "DOC"
            if extension in ext_dic:
                ext_dic[extension] += 1
            else:
                ext_dic.update({extension: 1})
            # s =  file.rsplit('_', 2)
            # print(s) # debug
            # print("Year:",s[1][0:4]) # debug
            # year_file = s[1][0:4]
            # if year_file in year_dic:
            #    year_dic[year_file] += 1
            #else:
            #    year_dic.update({year_file: 1})
            # get court
            court_name = court_get_by_file(file, list_court)
            if court_name in court_dic:
                court_dic[court_name] += 1
            else:
                court_dic.update({court_name: 1})
            i+=1
            print()
        total+=i # global total
        year_dic.update({year: i})
        if i == 0:
            print("-> directory empty")
            print()

# stats: court, year, file extension

print("Total files:", total)
print()

# Show dic stats
print("Court stats:")
print()
dic_show(court_dic, "court")

print("Year stats:")
print()
dic_show(year_dic, "year")

print("File extensions stats:")
print()
dic_show(year_dic, "file extensions")

# Save dic stats
file_name = 'sentences_by_court_stats.csv'
path_out = sentences_stat_dir + os.sep + file_name
print("Saving ditionary to: '", path_out,"'")
dic_save(court_dic, file_name)
print("done!")
print()

file_name = 'sentences_by_year_stats.csv'
path_out = sentences_stat_dir + os.sep + file_name
print("Saving ditionary to: '", path_out,"'")
dic_save(year_dic, file_name)
print("done!")
print()

file_name = 'sentences_by_ext_stats.csv'
path_out = sentences_stat_dir + os.sep + file_name
print("Saving ditionary to: '", path_out,"'")
dic_save(ext_dic, file_name)
print("done!")
print()


end_time = datetime.now().replace(microsecond=0)
print("***")
print("End process:", end_time)
print("Time to finish:", end_time - start_time)
print()
