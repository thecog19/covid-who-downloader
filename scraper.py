import requests
from bs4 import BeautifulSoup
import csv 
from crossref.restful import Works
import time



def main(path, target="../covid", mode="files"):
  print("Initalizing scraping in " + mode +  "\n")
  collection = Works()
  scrape(path, collection)

def scrape(path, collection):
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
        download_url(url)
      if(count % 100 == 0):
        print(count)
    print("Scraped!")

def download_url(url):
  session = requests.Session()
  time.sleep(10)
  res = session.get(url)
  content = res.content
  print(content)


main("csv.csv")