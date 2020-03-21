# Created March 21st, 2020.
# Last updated March 21st, 2020.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located, visibility_of_element_located, invisibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
import time
	
# The first time this button is clicked per session:
# 	- Go into Firefox preferences, set the download location to the desired folder.
#	- Check 'Do this automatically for files of this type from now on'.

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
		
driver = webdriver.Firefox()
process_webpage(driver, "http://dx.doi.org/10.1002/jmv.25767", "online-library.wiley.com")
process_webpage(driver, "https://academic.oup.com/qjmed/advance-article/doi/10.1093/qjmed/hcaa089/5809152", "academic.oup.com")
