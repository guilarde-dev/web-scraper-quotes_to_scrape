##  🌟 Quotes Web Scraper | Pythonic Effort 

  robust and automated web scraping built with __Python__ and __Selenium__. the script extracts data from quotes.toscrape.com and persists collected data to multiple professional formats.

##  🛠️ Features

  * __Automated data extraction__: extract the author's name, quote, link to see about the author and the datetime of the extraction
  * __filter of author__: this script persists the quotes of the authors that are in the filter of the file config.json, can be changed to other authors but need to put capital letter in begging of the name and surname.
    __example__: the filter "authors": ["Albert Einstein", "J.K. Rowling" ] does the code just take quotes of Albert Einstein and J.K. Rowling.
  * __anti-bot detection__: integrated with Selenium-Stealth and Options to doesn´t be detected.
  * __logging library__: integrated with comprehensive logging for real-time monitoring and error tracking.
  * __error handling__: uses blocks of try and except to try again if an error happen and be robust.
  * __multi-format persistence__:
    *__local__: save data to .csv and .xlsx files.
    *__cloud__: syncs data to _google sheets_ spreadsheets

##  📋 setup and prerequisites

  __google sheets integration__: to the script storage the data correctly, follow these steps:
     __open file__: open a new planner in google sheets and rename it as
    
  
    
