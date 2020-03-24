import requests
from bs4 import BeautifulSoup
import csv 
from crossref.restful import Works
import time
import pdfkit 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located, visibility_of_element_located, invisibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", "/home/felipe/programing/python/covid")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
firefox = webdriver.Firefox(profile)


firefox.set_page_load_timeout(60)
def main(path, target="../covid", mode="files"):
  print("Initalizing scraping in " + mode +  "\n")
  collection = Works()
  scrape(path, collection, target)

def scrape(path, collection, target):
  print("loading csv!")
  
  with open(path, 'r') as file:
    print("CSV Open! Initalizing scrape!")
    reader = csv.reader(file)
    count = 0
    for row in reader:
      count += 1
      doi = collection.doi(row[10])
      if(doi != None):
        url = doi.get("URL", "")
        if(url != ""):
          try: 
            download_url(url, target, row[0].replace("/", "<replace>"))
          except Exception as e:
            print(url) 
            print(e)
      if(count % 100 == 0):
        print(count)
    print("Scraped!")

def download_url(url, target, title):
  session = requests.Session()
  try: 
    res = session.get(url)
    domain = res.url.split("/")[2]
    if domain == "linkinghub.elsevier.com":
      res2 = requests.get(url)
      soup = BeautifulSoup(res2.text, features="html.parser")
      ele = soup.find("input")
      url2 = ele.get("value").replace('%2F', "/").replace('%3A', ":")
      domain = url2.split("/")[2]
      res = session.get(url2)
  except Exception as e: 
    print("selenium time")
    try:
      process_webpage(firefox,url,"")
    except Exception as e:
      print("selenium error")
      print(e)
    return 
  if(res.status_code == 200):
    content = res.content 
    soup = BeautifulSoup(content, features="html.parser")
    path = target + "/" + title + ".pdf"
    if(domain == "link.springer.com"):
      link = soup.findAll("a", {"class": "c-pdf-download__link"})[0]
      pdf = requests.get("https:" + link.get('href'))
      open(path, 'wb').write(pdf.content)
    elif(domain == "journal.yiigle.com"):
      #chinese language articles, many of which have been removed
      return
    elif(domain == "www.thelancet.com"):
      link = soup.findAll("a", {"class": "article-tools__item__pdf"})[0]
      pdf = requests.get("https://www.thelancet.com" + link.get('href'))
      open(path, 'wb').write(pdf.content)
    elif(domain == "www.bmj.com"):
      link = soup.findAll("a", {"class": "pdf-link"})[0]
      pdf = requests.get("https://www.bmj.com" + link.get('href'))
      open(path, 'wb').write(pdf.content)
    elif(domain == "www.sciencemag.org"):
      pdfkit.from_url(url, path) 
    elif(domain == "www.nature.com"):
      link = soup.findAll("a", {"data-track-label": "PDF download"})[0]
      pdf = requests.get("https:" + link.get('href'))
      open(path, 'wb').write(pdf.content)
    elif(domain == "www.tandfonline.com"):
      link = soup.findAll("a", {"class": "show-pdf"})[0]
      pdf = requests.get("https://www.tandfonline.com" + link.get('href'))
      open(path, 'wb').write(pdf.content)



  
# The first time this button is clicked per session:
#   - Go into Firefox preferences, set the download location to the desired folder.
# - Check 'Do this automatically for files of this type from now on'.

def process_webpage(driver, page, domain):
  if domain == 'onlinelibrary.wiley.com':
    driver.get(page)
    time.sleep(5)
    pdfButton = driver.find_element_by_link_text("PDF")
    pdfButton.click()
    time.sleep(5)
    pdf_container = driver.find_element_by_id('pdf-iframe')
    iframe_url = pdf_container.get_attribute('src')
    driver.get(iframe_url)
    time.sleep(5)
    downloadButton = driver.find_element_by_id('download')
    downloadButton.click() 
  elif domain == 'academic.oup.com':
    driver.get(page)
    time.sleep(5)
    pdfButton = driver.find_element_by_link_text("PDF")
    pdfButton.click()
    time.sleep(5)
    downloadButton = driver.find_element_by_id('download')
    downloadButton.click()
  else:
    driver.get(page)
    time.sleep(5)
    pdfButton = driver.find_element_by_link_text("PDF")
    pdfButton.click()
    try:
      downloadButton = driver.find_element_by_id('download')
      downloadButton.click()
    except:
      pdf_container = driver.find_element_by_id('pdf-iframe')
      iframe_url = pdf_container.get_attribute('src')
      driver.get(iframe_url)
      time.sleep(5)
      downloadButton = driver.find_element_by_id('download')
      downloadButton.click()
    time.sleep(10)


main("csv.csv")
# download_url("http://dx.doi.org/10.1007/s11604-020-00948-y", "../covid", "felipe")
