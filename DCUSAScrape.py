from DCUSAScript import Scraper
from selenium.webdriver.common.keys import Keys
from ScrapeTools import xpathCheck
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import os
from send_mail import sendMail
import ftplib
import atexit

def exit_handler():
  subject = 'Absupply Services DCUSA Scrape crashed'
  to =  'liz.absupply@gmail.com,randall@stokesweb.com,thomas.staats443@gmail.com,rhoward@absupply.net'
  html = f"DCUSA Scrape crashed"
  print(html)
  sendMail(html,subject,to)

atexit.register(exit_handler)

email = "rhoward@absupply.net"
password = "Frodo001!"
techHub = "https://techhub.doorcontrolsusa.com/"

exactSearchSilder ="/html/body/div/header/div[3]/div/div[3]/ul/li[3]/div/div/section[2]/div[2]/div/div/div[1]/div/label[1]/span"
#exactSearchSilder2 ="/html/body/div/header/div[3]/div/div[3]/ul/li[3]/div/div/section[2]/div[2]/div/div/div[1]/div/label[1]/input"
#exactSearchSilder3 ="/html/body/div/header/div[3]/div/div[3]/ul/li[3]/div/div/section[2]/div[2]/div/div/div[1]/div/label[1]"

exactSearchItem = "/html/body/div/header/div[3]/div/div[3]/ul/li[3]/div/div/section[2]/div[2]/div/div/div[2]/div[1]/div/div[1]/div"

listPrice = "/html/body/div[1]/main/main/section[1]/div/div[1]/form/div[1]/dl/div[1]/dd/span"
netPrice = "/html/body/div[1]/main/main/section[1]/div/div[1]/form/div[1]/dl/div[2]/dd/span"
stock = "/html/body/div[1]/main/main/section[1]/div/div[1]/form/div[1]/dl/div[3]/dd/span"
skuOnPage = "/html/body/div[1]/main/main/section[1]/div/div[1]/div[2]/h1"
moreStockDataButton = "/html/body/div[1]/main/main/section[1]/div/div[1]/form/div[1]/dl/div[3]/dd/span/div/button"
moreStockDataTable = "/html/body/div[2]/div/div/div[2]/table"
totalStock = "/html/body/div[2]/div/div/div[1]/dl/dd[3]"
def ftp_stock_data():
  try:
    print("attemping file send")
    session = ftplib.FTP('hypv8096.appliedi.net','importexportuser','vHj34#yWxff@44')
    #session = ftplib.FTP('hypv8096.appliedi.net','CRLaurenceUser','vBB3434@zj#jhv@2')
    file = open('DCUSAStock.csv','rb')# file to send
    print(session,"<session file>",file)
    print(session.storbinary('STOR import/DCUSAStock.csv', file))     # send the file
    print("sending...")
    sleep(2)
    file.close()     
    # Enter File Name with Extension
    filename = "export/DoorControlsExport.csv"
  
    # Write file in binary mode
    with open("DoorControlsExport.csv", "wb") as file:
        # Command for Downloading the file "RETR filename"
        session.retrbinary(f"RETR {filename}", file.write)# close file and FTP
    file.close()
    session.quit()
  except Exception as e:
    print("FTP SEND FAILED")
def scrapeSingleSku(sku,productID):
  
  print("scraping sku")
  data =  {"SKU":sku,"ProductID":productID}
  sleep(1)
  try:
    client.driver.get("https://www.doorcontrolsusa.com")
    sleep(1)                 
    try:
      searchBar = "/html/body/div/header/div[3]/div/div[3]/ul/li[3]/div/div/section[1]/div/div/input"
      searchEle = xpathCheck(searchBar,client.driver)
      searchEle.clear()
      searchEle.send_keys(sku)
      searchEle.send_keys(Keys.ENTER)
      sleep(1)
    except:
      client.init_driver()
      loginDcusa()
      print("could not find search bar")
      scrapeSingleSku(sku,productID)
    try:
      exactSearchEle = xpathCheck(exactSearchSilder,client.driver)  
      exactSearchEle.click()
      print("clicking exact slider1")
      sleep(1.5)
    except:
      print("couldnt find exact search slider")

    if "NO ITEMS" in client.driver.page_source: 
      data['stock_data'] = "Item not on DCUSA or discontinued"
      return data     
    
    try:
      itemEle = xpathCheck(exactSearchItem,client.driver)
      itemEle.click()
    except:
      print("went straight to item?")
         
    try:
      skuOnPageEle = xpathCheck(skuOnPage,client.driver)
      skuFromPage = skuOnPageEle.text
      print(f"{sku=} {skuFromPage=}")
      data['list_price'] = "none"
      data['net_price'] = "none"
      if not sku == skuFromPage: return data
    except:
      print("skuOnPage not found")
    try:
      listPriceEle = xpathCheck(listPrice,client.driver)
      data['list_price'] = listPriceEle.text
      print(f"Found list_price {data['list_price']=}")
    except:
      data['list_price'] = "none"
    try:
      netPriceEle = xpathCheck(netPrice,client.driver)
      data['net_price'] = netPriceEle.text
      print(f"Found net_price {data['net_price']=}")
    except:
      data['net_price'] = "none"
    try:
      stockEle = xpathCheck(stock,client.driver)
      data['stock_status'] = stockEle.text
      print(f"Found stock {data['stock_status']=}")
    except:
      data['stock_status'] = "none"
    #try:
    if data['stock_status'] == "Ready to Ship":
      try:
        moreStockButtonEle = xpathCheck(moreStockDataButton,client.driver) 
        moreStockButtonEle.click()
        print(f"Found more stock data")
      except:
        data['stock_data'] = "none"
        return data
      try:
        moreStockTableEle = xpathCheck(moreStockDataTable,client.driver)
        data['stock_data'] = moreStockTableEle.text.replace('\n','~').replace("Warehouse Number in Stock~","")       
      except:
        data['stock_data'] = "none"        
      try:
        moreStockTableEle = xpathCheck(totalStock,client.driver)
        data['stock_total'] = moreStockTableEle.text       
      except:
        data['stock_total'] = "none"
        
    else:
      data['stock_data'] = "none"
      data['stock_total'] = "none"
    return data
  except:
    client.init_driver()
    loginDcusa()
    
def loginDcusa():
  print("Logging in")
  try:
    client.driver.get("https://www.doorcontrolsusa.com/account/login")
    sleep(1)
    emailBar = "/html/body/div/main/section/div/form/div[1]/input"
    emailEle = xpathCheck(emailBar,client.driver)
    passBar = "/html/body/div/main/section/div/form/div[2]/input"
    passEle = xpathCheck(passBar,client.driver)
    emailEle.clear()
    passEle.clear()
    emailEle.send_keys(email)
    passEle.send_keys(password)
    passEle.send_keys(Keys.ENTER)
    # client.waitForElePGSingle("sss","Item details",client.driver.current_url,"Products/"+sku.replace(".",""))
  except:
    
    loginDcusa()



def productDataFromPgsrc(pgSrc):
  soup = BeautifulSoup(pgSrc, "html.parser")
  listPrice = "/html/body/div[1]/main/main/section[1]/div/div[1]/form/div[1]/dl/div[1]/dd/span"
  netPrice = "/html/body/div[1]/main/main/section[1]/div/div[1]/form/div[1]/dl/div[2]/dd/span"
  stock = "/html/body/div[1]/main/main/section[1]/div/div[1]/form/div[1]/dl/div[3]/dd/span"
  
def addsku(id,sku):
  dataList.append({"SKU":sku.replace(" ",""),"ProductID":str(int(id))})
while True:
  client = Scraper()
  dataList = []  
  loginDcusa()
  tr = 1/0
  df = pd.read_csv("DoorControlsExport.csv")
  df.apply(lambda row: addsku(row['ProductID'],row[" SKU"]),axis = 1)
  save_df = pd.DataFrame()
  # loadSkus = open("DCUSAProductCodes.txt", "r", encoding="utf8")
  # listOfSkus = loadSkus.readlines()
      # if sku+".html" in os.listdir("Products/"): 
      #   print("skip")
      #   continue
  count = 0
  save = 0
  print(f"{len(dataList)=}")
  for datas in dataList:
    sku = datas["SKU"]
    productID = datas["ProductID"]
    print(f"{count=}: {sku=}")
    try:  
      data = scrapeSingleSku(sku,productID)
      print(f"{data=}")
      save_df = save_df.append(data,ignore_index=True)
      count = count + 1
      if count > 10:
        save_df.to_csv('DCUSAStock.csv', index = False)
        save += 1
        count = 0
      
    except Exception as e:
      print(repr(e))
  ftp_stock_data()
  subject = 'Absupply Services Report'
  to =  'liz.absupply@gmail.com,randall@stokesweb.com,thomas.staats443@gmail.com,rhoward@absupply.net'
  html = f"DCUSAScrape Scrape Complete!"
  sendMail(html,subject,to)
