# Created March 21st, 2020.
# Last updated March 21st, 2020.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located, visibility_of_element_located, invisibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
import time

def get_pdf(driver):
	wait = WebDriverWait(driver, 5)
	containerLoaded = presence_of_element_located((By.ID, 'pdf-iframe'))
	wait.until(containerLoaded)
	pdf_container = driver.find_element_by_id('pdf-iframe')
	iframe_url = pdf_container.get_attribute('src')
	driver.get(iframe_url)
	time.sleep(5)
	downloadButton = driver.find_element_by_id('download')
	downloadButton.click() 
	
# The first time this button is clicked per session:
# 	- Go into Firefox preferences, set the download location to the desired folder.
#	- Check 'Do this automatically for files of this type from now on'.

def process_webpage(driver, page, domain):
	if domain == 'onlinelibrary.wiley.com':
		driver.get(page)
		wait = WebDriverWait(driver, 5)
		pdfButton = driver.find_element_by_link_text("PDF")
		pdfButton.click()
		get_pdf(driver)
	else:
		driver.get(page)
		wait = WebDriverWait(driver, 5)
		pdfButton = driver.find_element_by_link_text("PDF")
		pdfButton.click()
		get_pdf(driver)	

