#Pythonic Effort - Quotes Web Scraper
# Automated extraction from quotes.toscrape.com and persists data to multiple formats

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium_stealth import stealth
from datetime import datetime
import pandas as pd
import json
import logging
import os

logging.basicConfig(
    level= logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s ',
    handlers= [
        logging.FileHandler('quotes.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path_to_creds = os.path.join(BASE_DIR, "creds.json")

BASE_DIRE = os.path.dirname(os.path.abspath(__file__))
path_to_config = os.path.join(BASE_DIRE, "config.json")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_creds, scope)
client = gspread.authorize(creds)
planner = client.open("Planner quotes").sheet1

class Scraper:

    def open_json(self):
        with open(path_to_config, "r", encoding="utf-8") as f:
            self.informations = json.load(f)

    def __init__(self):

        self.open_json()

        self.url = self.informations["url"]
        self.datas = []
        self.bot = None

    def acess_site(self):
        while True:
            try:
                config = Options()
                config.add_argument("--headless")
                config.add_argument("--incognito")
                config.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36")
                self.bot = webdriver.Chrome(options=config)

                stealth(self.bot,
                    languages=["pt-BR", "pt"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,)
                
                logging.info('bot configurated with successfully.')
                
            except Exception:
                logging.error('detected error in config bot, trying again in 5 seconds')
                sleep(5)
                continue
        
            try:
        
                self.bot.get(self.url)
                logging.info('site acessed with successfully.')
                sleep(3)
                break

            except Exception:
                logging.error('error in acess site, trying again in 5 seconds.')
                sleep(5)
                continue

    def take_datas(self):
        wait = WebDriverWait(self.bot, 10)
        for item in range(10):
            try:
                boxes = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'quote')]")))
                for box in boxes:
                    sentence = box.find_element(By.XPATH, ".//span[contains(@class, 'text')]").text
                    author = box.find_element(By.XPATH, ".//small[contains(@class, 'author')]").text
                    about_author = box.find_element(By.XPATH, ".//span/a")
                    link = about_author.get_attribute('href')

                    quote = {
                        'quote': sentence,
                        'author': author,
                        'about': link,
                        'datetime': datetime.now().strftime("%d/%m/%Y %H:%M")
                        }

                    if quote not in self.datas:
                        if quote['author'] in self.informations["authors"]:
                            self.datas.append(quote)
                        else:
                            None
                        
            
            except Exception as e:
                logging.error(f'detected error in take_datas: {type(e).__name__}, trying again in 5 seconds.')
                sleep(5)
                continue

            try:
                button = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'next')]/a[contains(@href, '/page/')]")))
                button.click()
                logging.info('button clicked, going to next page.')
                sleep(3)
            except:
                logging.info('process of take datas finished.')
                break

        
        self.bot.quit()

    def save_datas(self, name_file="quotes.xlsx"):
        while True:
            try:
                df = pd.DataFrame(self.datas)
                df.to_excel(name_file, index=False)
                df.to_csv("quotes.csv", encoding="utf-8-sig", sep=";", index=False)
                google_datas = [list(item.values()) for item in self.datas]
                planner.append_rows(google_datas)
                logging.info('save datas concluded with successfully.')
                break

            except Exception:
                logging.critical('detected error in save_datas, trying again in 5 seconds.')
                sleep(5)
                continue

#object
test2 = Scraper()

#functions
test2.acess_site()
test2.take_datas()
test2.save_datas()
