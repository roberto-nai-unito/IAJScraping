# IAJScraping
Web scraper for the URL "https://www.giustizia-amministrativa.it/web/guest/dcsnprr"

1) Execute "01_scraper.py" to generate the list (index) of the sentences to be downloaded (index file in csv format saved in "sentences" folder); define in "01_scraper.py" the years needed to download.

2) Execute "02_downloader.py" to download the files indexed by "01_scraper.py" (using files csv saved in "sentences" folder).

3) Execute "03_analyzer.py" to get stats about the downloaded data (it analyze the /sentences directory and save stats in /sentences_stats).

NOTE: 
1) "log.py" and "sentence.py" are classes useful to the scripts "01_scraper.py";
2) Upon first execution, the script "01_scraper.py" creates the directory "sentences" where the list of sentences and their texts will be downloaded.
