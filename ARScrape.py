from ARScript import Scraper
from selenium.webdriver.common.keys import Keys
from ScrapeTools import xpathCheck, classCheck
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import os
from send_mail import sendMail
import ftplib
import atexit
client = Scraper()
def exit_handler():
  subject = 'AR Scrape crashed'
  to =  '<EMAIL>'
  html = f"AR Scrape crashed"
  print(html)
  sendMail(html,subject,to)

#atexit.register(exit_handler)
class Container:
  def __init__(self):
    self.listSet = []
  def addLink(self,link):
    self.listSet.append(link)
  def removeDuplicates(self):
    self.listSet = list(set(self.listSet))
boxThing = Container()

def parseLinks(pgSrc,container):
  soup = BeautifulSoup(pgSrc,"html.parser")
  a = soup.find_all("a",{"class":recipieATags})
  for href in a:
    #print(href['href'])
    container.addLink(str(href['href']))
  container.removeDuplicates()
  
  


recipieATags ="recipeCard__titleLink elementFont__titleLink margin-8-bottom"

def ftp_stock_data():
  try:
    print("attemping file send")
    #session = ftplib.FTP('host','user','pass')
    #file = open('ARStock.csv','rb')# file to send
    #print(session,"<session file>",file)
    #print(session.storbinary('STOR import/ARStock.csv', file))     # send the file
    #print("sending...")
    sleep(2)
    #file.close()     
  except Exception as e:
    print("FTP SEND FAILED")
def scrapeAll(links):
  
  print("scraping sku")
  data =  {}
  for each in links:
    print(f"{each=}")
    sleep(1)
    try:
      client.driver.get(each)
      sleep(1)                 
      try:
        for i in range(4):
          sleep(1)
          pgSrc = client.driver.page_source
          links = parseLinks(pgSrc,boxThing)
          try:
            loadmore = "category-page-list-related-load-more-button"
            loadmoreEle = classCheck(loadmore,client.driver) 
            loadmoreEle.click()
          except Exception as e:   
            print("1",repr(e))

        pgSrc = client.driver.page_source
        links = parseLinks(pgSrc,boxThing)
      except Exception as e:   
          print("2",repr(e))

        

      # if "NO ITEMS" in client.driver.page_source: 
      #   data['stock_data'] = "Item not on AR or discontinued"
      #   return data     

      
    except Exception as e:   
      print(repr(e))
  data['recipies'] = '~'.join(boxThing.listSet)
  return data
def loginAR():
  print("Logging in")
  client.init_driver()
  try:
    client.driver.get("https://www.allrecipes.com/recipes/200/meat-and-poultry/beef/")
    sleep(2)
    # emailBar = "/html/body/div/main/section/div/form/div[1]/input"
    # emailEle = xpathCheck(emailBar,client.driver)
    # passBar = "/html/body/div/main/section/div/form/div[2]/input"
    # passEle = xpathCheck(passBar,client.driver)
    # emailEle.clear()
    # passEle.clear()
    # emailEle.send_keys(email)
    # passEle.send_keys(password)
    # passEle.send_keys(Keys.ENTER)
    # client.waitForElePGSingle("sss","Item details",client.driver.current_url,"Products/"+sku.replace(".",""))
  except:
    
    loginAR()



def getRecipies():
  def addsku(link):
    dataList.append(link)
  dataList = []  
  loginAR()
  df = pd.read_csv("allRecipies.csv")
  df.apply(lambda row: addsku(row["link"]),axis = 1)
  save_df = pd.DataFrame()
  # loadSkus = open("ARProductCodes.txt", "r", encoding="utf8")
  # listOfSkus = loadSkus.readlines()
      # if sku+".html" in os.listdir("Products/"): 
      #   print("skip")
      #   continue
  count = 0
  save = 0
  print(f"{len(dataList)=}")
  
  #sku = datas["link"]
  #print(f"{count=}: {sku=}")
  try:  
    data = scrapeAll(dataList)
    print(f"{data=}")
    save_df = save_df.append(data,ignore_index=True)
    count = count + 1
    save_df.to_csv('ARStock.csv', index = False)
      
      
    
  except Exception as e:
    print(repr(e))
  #ftp_stock_data()
  subject = 'Services Report'
  to =  'thomas.staats443@gmail.com'
  html = f"ARScrape Scrape Complete!"
  sendMail(html,subject,to)
def parseRecipies():
  df = pd.read_csv("ARStock.csv")
  dataList = df.iloc[0,0].split('~')
  listOfLinks = [] 
  for link in dataList:
    listOfLinks.append(link)
    print(link) 
  return listOfLinks
listOfLinks = parseRecipies()

def scrapeRecipies(listOfLinks):
  pass