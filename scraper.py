import requests
from bs4 import BeautifulSoup
import csv 
import time
import json



def main(path, target="../covid", mode="files"):
  print("Initalizing scraping in " + mode +  "\n")
  scrape(path)

def scrape(path):
  print("loading csv!")
  
  with open(path, 'r') as file:
    print("CSV Open! Initalizing scrape!")
    reader = csv.reader(file)
    count = 0
    domain_count = {}
    resolve = 0
    for row in reader:
      count += 1
      res = requests.get("https://doi.org/api/handles/" + row[10])
      url = json.loads(res.content).get("values", [{}])[0].get("data", {}).get("value", "")
      if(url != ""):
        resolve += 1
        domain = url.split("/")[2]
        if domain == "journal.yiigle.com":
          print(row)
          print(url)
        if domain == "linkinghub.elsevier.com":
          res2 = requests.get(url)
          soup = BeautifulSoup(res2.text)
          ele = soup.find("input")
          url2 = ele.get("value")
          domain = url2.split("%2F")[2]
        if(domain_count.get(domain, "") == ""):
          domain_count[domain] = 1
        else:
          domain_count[domain] += 1
      if(count % 100 == 0):
        print(count)
    print("Scraped!")
    print(domain_count)

main("csv.csv")