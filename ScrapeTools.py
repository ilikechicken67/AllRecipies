from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#from ScrapeTools import downloadPageSource, waitForEle, xpathCheck, classCheck, idCheck 
def downloadPageSource(nameOfPage,html):
    
    fileToWrite = open(nameOfPage+".html", "w",encoding="utf-8")
    fileToWrite.write(html)
def readHtml(nameOfPage): 
    fileToWrite = open(nameOfPage, "r", encoding="utf8")
    return fileToWrite.read()
def waitForEle(driver, eleType, eleIdentifer, url, nameOfPage):
    driver.get(url)
    checkResults = None
    if eleType == "eleById":
        checkResults = idCheck(eleIdentifer)
    elif eleType == "eleByClass":
        checkResults = classCheck(eleIdentifer)
    elif eleType == "eleByXpath":
        checkResults = xpathCheck(eleIdentifer)
    else:
        print("error")
        return 0
    if checkResults == 0:
        print("Ele Not Found Or Check Logs")
    pageSource = driver.page_source
    downloadPageSource(nameOfPage,pageSource)
    return pageSource
def xpathCheck(path,driver):
    try:
        tempElement = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, path)) 
        ) 
        return tempElement 
    except Exception as e:
        print("No Element by that Xpath!")
        return 0
def xpathClick(path,client):
    try:
        tempElement = WebDriverWait(client.driver, 6).until(
            EC.presence_of_element_located((By.XPATH, path)) 
        ) 
        tempElement.click()
        pgSrc = client.driver.page_source
        start = time.time()
        while not "related-catalog-pages-summary" in pgSrc and time.time()-start<6: 
            pgSrc = client.driver.page_source
        if not "related-catalog-pages-summary" in pgSrc:
            return 0
        return pgSrc 
    except Exception as e:
        print("No Element by that Xpath!")
        return 0
def classCheck(path, driver):
    try:
        tempElement = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME , path)) 
        ) 
        return tempElement 
    except Exception as e:
        print("No Element by that Class Name!")
        return 0
def idCheck(path, driver):
    try:
        tempElement = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.ID, path)) 
        ) 
        return tempElement 
    except Exception as e:
        print("No Element by that ID")
        return 0

