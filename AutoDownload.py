# Idea:
# Automatically download script, kompakt and lsg of every day

import sys
from VorkursDownload import *
from selenium import webdriver

def exitWithError(error):
    logError(error)
    sys.exit(0)

def login(driver):
    driver.get(WebsiteToLogin)

    driver.find_element_by_xpath('//*[@id="f807"]').click()

    driver.find_element_by_xpath('//*[@id="name"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)

    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="sbmt"]'))

    try:
        driver.find_element_by_xpath('//*[@id="il_mhead_t_focus"]')
    except :
        exitWithError("Username or Password was invalid!")

    driver.get(WebsiteToCrawl)

def createDriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('prefs', {
        "download.default_directory": FolderToSaveTo + "\\DownloadTemp\\", #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    })
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    try:
        driver = webdriver.Chrome(options=options)
        driver.minimize_window()
    except :
        exitWithError("Webdriver not found, please check the chromedriver.exe, the Version of the driver and your Google Chrome")

    return driver

def main():
    print("Log File:", ErrorLogFilePath)
    print("\nStarting...\n")

    beforeStart()

    driver = createDriver()

    login(driver)

    beforeCrawl(driver)

    elements = getLinksToCrawl(driver)
 
    for text, link in elements:
        try:
            driver.get(link)
            crawl(driver, text, link)
        except Exception as e:
            logError("Error on Crawl Day: %s" % e)

    cleanup(driver)

if __name__ == "__main__":
    main()