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
    domain_count = {}
    error_tracker = {}
    for row in reader:
      count += 1
      doi = row[10]
      if(doi != ""):
        r = download_url("http://dx.doi.org/" + row[10])
        if(r["error"]):
          v = error_tracker.get(r["domain"], "")
          if(v != ""):
            error_tracker[r["domain"]] += 1
          else: 
            error_tracker[r["domain"]] = 1
        v = domain_count.get(r["domain"], "")
        if(v != ""):
          domain_count[r["domain"]] += 1
        else: 
          domain_count[r["domain"]] = 1


      if(count % 10 == 0):
        print(count)
    print("Scraped!")
    print(error_tracker)
    print(domain_count)

def download_url(url):
  domain = "error"
  code = 0
  try:
    session = requests.Session()
    res = session.get(url)
    content = res.content
    code = res.status_code
    domain = res.url.split("/")[2]
  except:

    print("Error error error")

  return_val = {}
  if(code == 403):
      return_val["domain"] = domain, 
      return_val["error"] = True
  elif(code == 0):
      return_val["domain"] = "doi", 
      return_val["error"] = True
  else:
      return_val["domain"] = domain, 
      return_val["error"] = False
  return  return_val



main("csv.csv")