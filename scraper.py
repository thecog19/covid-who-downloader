import requests
from bs4 import BeautifulSoup
import csv 
from crossref.restful import Works
import time



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
          download_url(url, target, row[0])
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
      soup = BeautifulSoup(res2.text)
      ele = soup.find("input")
      url2 = ele.get("value").replace('%2F', "/")
      domain = url2.split("%2F")[2]
      res = session.get(url2)
  except: 
    print("error")
    print(url)
    return 
  if(res.status_code == 200 and domain == "link.springer.com"):
    content = res.content
    soup = BeautifulSoup(content)
    link = soup.findAll("a", {"class": "c-pdf-download__link"})[0]
    pdf = requests.get("https:" + link.get('href'))
    open(target + "/" + title + ".pdf", 'wb').write(pdf.content)
  # elif(res.status_code == 200 and domain == )




main("csv.csv")
# download_url("http://dx.doi.org/10.1007/s11604-020-00948-y", "../covid", "felipe")