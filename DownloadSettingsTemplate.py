import os
import time
from Util import *

username = ""
password = ""

FolderToSaveTo = r"C:\Users"
ErrorLogFilePath = r"C:\Users\AutoDownloadError.log"

# Init Utility functions
initUtil(FolderToSaveTo, ErrorLogFilePath)

WebsiteToCrawl = ""
WebsiteToLogin = ""

# Remove Files from last run, prepare, etc.
def beforeStart():
    pass

# Prepare website before extracting links to crawl
def beforeCrawl(driver):
    pass

# Return a list of (Title of Website, link to website) of sites to Crawl
def getLinksToCrawl(driver) -> list:
    pass
 
# Crawl a Site. Site has been loaded before
def crawl(driver, text: str, link: str):pass

# After crawling cleanup Files
def cleanup(driver):
    pass