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
    for row in reader:
      count += 1
      res = requests.get("https://doi.org/api/handles/" + row[10])
      url = json.loads(res.content).get("values", [{}])[0].get("data", {}).get("value", "")
      print(json.loads(res.content).get("values", [{}])[0].get("data", {}))
      if(url != ""):
        download_url(url)
      if(count % 100 == 0):
        print(count)
    print("Scraped!")

def download_url(url):
  print(url)
  try:
    res = requests.get(url)
    content = res.content
    print(content)
  except:
    print("error")

main("csv.csv")