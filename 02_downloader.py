# 02_downloader.py

# DOWNLOADER: from the csv execute the wget and save it

from datetime import datetime

import os
from os import path

import pandas as pd
# pip install pandas

### GLOBALS ###

sentence_dir = "sentences" # <-- INPUT
file_donwloaded = 0 # total file downloaded from the wget
file_not_needed = 0 # total file already saved in filse system (fs)


def data_load(file_name):
    """ Given a csv file_name, load it into a pandas Dataframe; key_index is the custom index of the DF """    
    path_input = sentence_dir + os.sep + file_name
    print()
    print("Reading csv input:", path_input)
    print()
    input_df = pd.read_csv(path_input, delimiter = ";", low_memory = False, header = None, usecols = [9,10]) # usecols = [9,10] -> URL and FILENAME
    print("...done!")
    print() 

    # Search for duplicate rows and count them
    if input_df.duplicated().sum() > 0:
        print("Rows duplicated (to be deleted): ", input_df.duplicated().sum())
        print()
        # Search for duplicate rows and delete them
        # input_df = input_df.drop_duplicates()

    return input_df


def data_show(input_df):
    """ Given a pandas Dataframe, show the data """
    print("-> Dataframe description:")
    print()
    print("Dataframe length (rows):", len(input_df)) # Show number of rows
    print()
    print("Dataframe shape (rows, cols):", input_df.shape) # Show rows,cols number
    print()
    print("Dataframe columns:", input_df.columns) # Show columns (features)
    print()
    print("Column types:") 
    print()
    print(input_df.dtypes.value_counts()) # Column types
    print()
    print(input_df.head()) # Show first 10 rows
    print("...")
    print(input_df.tail()) # Show last 10 rows
    print()

def get_sentence_file(url_download, file_donwload, year):
    """ Download the sentence file """
    global file_donwloaded
    global file_not_needed
    path_file = sentence_dir + os.sep + str(year) + os.sep + file_donwload
    if (path.exists(path_file) == False): # if the sententce file doesn't exists do the wget and move
            file_donwloaded+=1
            command = "wget --no-check-certificate -O \"" + path_file + "\" \"" + url_download + "\""
            os.system(command)
            print("File downloaded")
    else: # avoid the wget
            file_not_needed+=1
            print("File already downloaded")


### MAIN ###
print()
print("*** WEB SCRAPER / DOWNLOADER ***")
start_time = datetime.now().replace(microsecond=0)
print()
print("Start process:", start_time)
print()

year_start = 2007 # <-- INPUT
year_end = 2023 # <-- INPUT (excluded)

for year in range(year_start, year_end):

    file_input = str(year) + "_sentences.csv" 

    print("Year:", year)
    print("File with index:", file_input)

    # create the directory for download
    path_year = sentence_dir + os.sep + str(year)
    if not os.path.exists(path_year):
        os.makedirs(path_year)

    input_df = data_load(file_input)

    print("Input DF:")
    print()
    data_show(input_df)
    print()

    n = len(input_df)

    i = 0

    for row in input_df.itertuples():
        print("[",i,"/",n,"] - year:", year)
        url_download = row[1]
        file_donwload = row[2]
        print("URL:", url_download)
        print("File:", file_donwload)
        get_sentence_file(url_download, file_donwload, year)
        print()
        i+=1


end_time = datetime.now().replace(microsecond=0)
print("***")
print("End process:", end_time)
print()
print("Time to finish:", end_time - start_time)
print()
