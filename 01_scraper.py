# 01_scraper

# WEB SCRAPER to get the list of filew to be downloaded

import mechanicalsoup
# pip install MechanicalSoup

from bs4 import BeautifulSoup as bs
# pip install beautifulsoup4

import pandas as pd
# pip install pandas

from datetime import datetime

import os
from os import path

from sentence import Sentence # local Class

import sys
# print(sys.getrecursionlimit())

from log import * # local class

# Global parameters

import re

### GLOBALS ###

sys.setrecursionlimit(30000)

# query string
input_search = "appalt*" # <-- INPUT: text input to search in IAJ
year_search = 2022 # <-- # INPUT (year of the sentences searched)

# URLs
paging = 60 # number of results per page
page_increment = 1 # <-- input to start from a defined page (shift -> move the response of page + page_increment) starting always from 0
# page_increment = 4155
url_search = "https://www.giustizia-amministrativa.it" # new IAJ website
# url_search = "https://www.giustizia-amministrativa.it/web/guest/dcsnprr" # old
url = "https://www.giustizia-amministrativa.it"
total_results = 0  # total numbers of results
total_pages = 0 # total pages to be parsed

# sentences
sentence_dir = "sentences" # csv and file
sentence_file_name = "sentences.csv"
sentence_download_count = 0 # global number of sentences downloaded
sentence_url_list =[]
sentence_list_obj =[]
# csv_result_header = "ID (cig, gara, accordo); tipo_ID; codice_ecli; provvedimento_titolo; provvedimento_tipo; sentenza_numero; tribunale_codice; tribunale_citta; tribunale_sezione; ricorso_numero; sentenza_url; sentenza_file"
csv_result_header = "pagina;codice_ecli;provvedimento_titolo;provvedimento_tipo;sentenza_numero;tribunale_codice;tribunale_citta;tribunale_sezione;ricorso_numero;sentenza_url;sentenza_file"
search_type = ""

def get_administrative_judgment(text_to_search, page, year_search): 
    """ Compile and submit the IAJ form: text_to_search is the querystring, page = 0 is the first page of results """
    global paging
    global browser
    global total_pages

    form_id = "_GaSearch_INSTANCE_2NDgCF3zWBwk_provvedimentiForm"

    try:
        browser.select_form('form[id="'+form_id+'"]') # get the form data by id
        # print(browser.get_current_form().print_summary()) # get the content of the form

        browser["_GaSearch_INSTANCE_2NDgCF3zWBwk_searchtextProvvedimenti"] = text_to_search # textbox

        browser["_GaSearch_INSTANCE_2NDgCF3zWBwk_pageResultsProvvedimenti"] = paging # selectbox

        browser["_GaSearch_INSTANCE_2NDgCF3zWBwk_TipoProvvedimentoItem"] = "Sentenza" # selectbox

        browser["_GaSearch_INSTANCE_2NDgCF3zWBwk_DataYearItem"] = str(year_search) # selectbox

        # _GaSearch_INSTANCE_2NDgCF3zWBwk_DataYearItem

        if (page == 0):  # if it's the first time, save the number of results
            response = browser.submit_selected()
            html_content = bs(response.text, 'html.parser')
            res_num = int(html_content.strong.string) # results number
            total_results = res_num
            # Pages goes to 0 to n (visualized in the web page as 1 to n+1)
            # total_pages = int(res_num/paging) + int(res_num%paging) # number of the pages to be parsed (not working)
            temp_last_page_1 = html_content.find_all('li', {'class':'pagination-li'}) # [-1] contains the last page
            # print("temp_last_page 1:", temp_last_page_1[-1]) # debug
            for tag in temp_last_page_1[-1].find_all('a'):
                try:
                    if re.match('changePage',tag['onclick']):           # if onclick attribute exist, it will match for changePage, if success will print
                        # print("Last page object:", x['onclick'])      # debug
                        onclick = tag['onclick']                        # string value inside onclik
                        onclick_value = re.findall("[0-9]+",onclick)    # get the numbers inside the Javascript function (is a list)
                        last_page = int(onclick_value[0])
                        # print("Last page value:", str(l_page))        # debug
                        total_pages = last_page
                except:
                    pass
            log_writer("Text to search: " + str(text_to_search))
            log_writer("Year to search: " + str(year_search))
            print("Results found via URL:", str(res_num))
            print("Paging:", str(paging))
            print("Page shift:", str(page_increment))
            print("Total pages to be parsed:", str(total_pages))
            log_writer("Results found via URL: " + str(res_num))
            log_writer("Paging: " + str(paging))
            log_writer("Page shift: " + str(page_increment))
            log_writer("Total pages to be parsed: " + str(total_pages))
            log_writer("Page: " + str(page))
            print()

        # if element "_GaSearch_INSTANCE_2NDgCF3zWBwk_step" is not available, LinkNotFoundError happens
        if (page != 0):
            browser["_GaSearch_INSTANCE_2NDgCF3zWBwk_step"] = page # textbox
            log_writer("Page: " + str(page))
            response = browser.submit_selected()

        response_parser(text_to_search, response, page, year_search) # parse the results (response) for the text_to_search

    except mechanicalsoup.LinkNotFoundError as e:
        print("LinkNotFoundError trying to connect to '",url_search, "' (to form elements too)")


def response_parser(text_to_search, response, page, year_search):
    """ Read the response of the browser """
    global url_search
    global url
    global search_type
    # global csv_result_file
    global sentence_url_list
    global sentence_list_obj
    global paging
    global sentence_download_count
    global total_results
    global page_increment
    global total_pages

    # print('Response:\n', response.text)

    count = 0 # local count for paging

    sentence_list_obj = [] # reset the list of found sentence
    sentence_url_list = [] # reset the list of URL

    html_content = bs(response.text, 'html.parser')

    articles_num = len(html_content.findAll("article")) - 1 # -1 because the last article is not a sentence

    print("Articles (number of sentences) in this page:", str(articles_num))

    print()

    # for each <article> (a sentence) extract the data (location, link, ECLI, etc...)
    for article in html_content.findAll("article"):
        count+=1 # increment local count of download (for the paging)
        sentence_download_count+=1 # increment global count (for the whole download)

        # if (count > paging): # it it's over the paging save it to csv (does not work fot he last page with less articles)
        if (count > articles_num):
            print("Results parsed for this page:", count-1)
            print("-> Total sentences parsed until this page:", sentence_download_count-1)

            # write sentences to CSV
            print("Writing CSV file sentences...")
            for a_sentence in sentence_list_obj:
                sentence_csv = a_sentence.toCSV() # stream a sentence from obj to csv string

                file_name = str(year_search) + "_" + sentence_file_name
                csv_file_path = sentence_dir + os.sep + file_name

                with open(csv_file_path, mode="a") as fp:
                    fp.write(str(page) + ";" + sentence_csv + os.linesep)
                    # t_sentence = (a_sentence.sentence_url, a_sentence.sentence_filename) # tuple for the download (URL and filename)
                    # sentence_url_list.append(t_sentence)

            print()

            # submit a new page
            if (page == 0): # if it's in page 0, move of a shift to start to a new paging, else move of 1
                page = page + page_increment
            else:
                page = page + 1

            print()
            print("New page -->", str(page))

            if (page > total_pages): # if the new page it's over the total pages stop it
                print("Web scraper finished")
                print("Year:", year_search)
                print()
                quit()
            else:
                get_administrative_judgment(text_to_search, page, year_search)

        sentence = Sentence() # create a new sentence object and extract the data from <article>

        print("Result [",str(count),"] / page [",str(page),"]")
        # print(type(article.get("class"))) # the class is a list so [0] is the first attribute searched
        if (article.get("class")[0] == "ricerca--item"):
            for link in article.findAll("a"):
                if (link.get("data-sede") != None):
                    # print(link["data-sede"]) # code of the tribunal
                    sentence.tribunal_code = link["data-sede"]
                    # print(link["href"])
                    sentence.sentence_url = url + link["href"]
                    string_href = link["href"].split("&")
                    string_file_name = string_href[3].split("=")
                    string_file = link["data-sede"] + "_" + string_file_name[1]
                    # print(string_file)
                    sentence.sentence_filename = string_file
        div_count = 0
        for div in article.findAll("div", {"class": "col-sm-12"}):
            div_count+=1
            if (div_count==1): # title from the second div
                a_count = 0
                for ahref in div.findAll("a"):
                    a_count+=1
                    if (a_count==2):
                        # print(ahref.string)
                        sentence.sentence_title = ahref.string
            if (div_count==2): # type, city, section, number
                # print(div)
                bcount = 0
                for b in div.findAll("b"):
                    bcount+=1
                    # print(b.string)
                    if (bcount==1):
                        sentence.sentence_type = b.string
                    if (bcount==2):
                        sentence.tribunal_city = b.string
                    if (bcount==3):
                        sentence.tribunal_section = b.string
                    if (bcount==4):
                        sentence.sentence_number = b.string
            # div_count==3 not needed
            if (div_count==4): # recourse number
                # print(div)
                for b in div.findAll("b"):
                    # print(b.string)
                    sentence.recourse_number = b.string
            if (div_count==5): # ecli
                # print(div)
                for b in div.findAll("b"):
                    # print(b.string)
                    sentence.sentence_ecli = b.string
            else:
                sentence.sentence_ecli = None

        print(sentence.toString())
        if (page==0): # it is the first running (page_increment = 1), the page 0 is needed in the list
            if (page_increment==1):
                sentence_list_obj.append(sentence) # add a sentence to the list
        else:
            sentence_list_obj.append(sentence) # add a sentence to the list

### MAIN ###
print()
print("*** WEB SCRAPER / INDEXER ***")
print()
start_time = datetime.now().replace(microsecond=0)
log_manager(start_time, year_search)
log_writer("Start process: " + str(start_time))
print("Start process:", start_time)
print()

browser = mechanicalsoup.StatefulBrowser() # web scraper object
browser.open(url_search)
browser.follow_link("dcsnprr") # moves to https://www.giustizia-amministrativa.it/web/guest/dcsnprr
print("URL:",browser.get_url())
print()
print("Year:",year_search)
print()
print("Query:",input_search)
print()

# create the directories for every year
path_year = sentence_dir + os.sep + str(year_search)
if not os.path.exists(path_year):
    os.makedirs(path_year)

get_administrative_judgment(input_search, 0, year_search)

end_time = datetime.now().replace(microsecond=0)
print("***")
print("End process:", end_time)
print()
log_writer("End process: " + str(end_time))
print("Time to finish:", end_time - start_time)
print()
log_writer("Time to finish: " + str(end_time - start_time))

