import pandas as pd
import numpy as np
import time
from time import sleep
from pandas.core.frame import DataFrame
import selenium
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import ftplib
from bs4 import BeautifulSoup
from pprint import pprint
from inspect import currentframe
import logging

##### LOCAL
from ScrapeTools import downloadPageSource, waitForEle
#####

####
logger = logging.getLogger("AR")
hdlr = logging.FileHandler("AR.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.info('Scrape started')
####

class Scraper():
    def __init__(self):
        print("initializing Scraper")
        self.count = 0
        self.save = []
        self.loop = True
        #self.all_categories = get_main_nav_categories()    
        self.subCategories = []     
        self.init_driver()
        print("Scraper initialized ")
    def init_driver(self):
        try:
            sleep(2)
            self.driver.close()
            sleep(2)
            self.driver.quit()
            sleep(2)
            print("Closed Current Driver, Initializing fresh one")
        except:
            print("No Current Driver, Initializing fresh one")
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.44 Safari/537.36")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument('log-level=3')
        #chrome_options.add_argument("--no-sandbox") # linux only
        #chrome_options.add_argument("--headless") #ERR_TOO_MANY_REDIRECTS
        chrome_options.headless = True # also works
        self.driver = webdriver.Chrome(options=chrome_options)
        #driver = webdriver.Firefox()
        self.driver.delete_all_cookies()
        sleep(5)
    def waitForElePGSingle(self, eleType, eleIdentifer, url, nameOfPage):
        eleFound = False
        start = time.time() 
        try:
          self.driver.get(url)    
        except:
            sleep(1)
            self.driver.close()
            sleep(2)
            self.driver.quit()
            sleep(2)
            self.driver = None
            sleep(.5)
            self.init_driver()
            sleep(2)
            start = time.time()
            self.driver.get(url)       
        pgSrc = self.driver.page_source
        while not eleFound:      
            if eleIdentifer in pgSrc and not "Log in to view" in pgSrc:        
               eleFound = True
               if eleType == "product": 
                   
                   self.driver.save_screenshot("images/"+nameOfPage+".png")
               print("Screenshot???")
               break                        
            elif (time.time() - start) > 10 or "Log in to view" in pgSrc:
                #if "To continue br.... " in pgSrc baneetsSwitchVpnIP() 
                if not "Log in to view" in pgSrc:       
                  downloadPageSource(nameOfPage,pgSrc)
                  eleFound = True
                  print("eleMaybeFound")
                  break    
                pgSrc = self.driver.page_source
                sleep(1)
                self.driver.close()
                sleep(2)
                self.driver.quit()
                sleep(2)
                self.driver = None
                sleep(.5)
                self.init_driver()
                sleep(2)
                start = time.time()
                return 0
                # self.driver.get(url)
                # pgSrc = self.driver.page_source
            else:
                pgSrc = self.driver.page_source
        #if not "To continue browsing, please log in" in pgSrc:   
        #downloadPageSource(nameOfPage,pgSrc)
        return pgSrc
    def waitForElePG(self, eleType, eleIdentifer, url, nameOfPage):
        eleFound = False
        start = time.time() 
        self.driver.get(url)         
        pgSrc = self.driver.page_source
        while not eleFound:  
            for identifiers in eleIdentifer:    
                if identifiers in pgSrc and not "To continue browsing, please log in" in pgSrc:        
                    eleFound = True
                    print("eleFound")
                    break                        
                elif (time.time() - start) > 6 or "To continue browsing, please log in" in pgSrc:
                    #if "To continue br.... " in pgSrc baneetsSwitchVpnIP() 
                    pgSrc = self.driver.page_source
                    sleep(1)
                    self.driver.close()
                    sleep(2)
                    self.driver.quit()
                    sleep(2)
                    self.driver = None
                    sleep(.5)
                    self.init_driver()
                    sleep(2)
                    start = time.time()
                    self.driver.get(url)
                    pgSrc = self.driver.page_source
                else:
                    pgSrc = self.driver.page_source
        #if not "To continue browsing, please log in" in pgSrc:   
        downloadPageSource(nameOfPage,pgSrc)
        return pgSrc
