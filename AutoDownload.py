# Idea:
# Automatically download script, kompakt and lsg of every day

import os
import sys
import time
import glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

username = input("Enter your KIT-ILIAS Username: ")
password = input("Enter your KIT-ILIAS Password: ")

print("\nStarting...\n")

def login(driver):
    url = "https://ilias.studium.kit.edu/login.php?target=crs_1235442&client_id=produktiv&cmd=force_login&lang=de"

    driver.get(url)

    driver.find_element_by_xpath('//*[@id="f807"]').click()

    driver.find_element_by_xpath('//*[@id="name"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)

    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="sbmt"]'))

    try:
        driver.find_element_by_xpath('//*[@id="il_mhead_t_focus"]')
    except :
        print("Username or Password was invalid!")
        time.sleep(3)
        sys.exit(0)

    return 

def deleteFolder(dir):
    if os.path.exists(os.getcwd() + dir):
        os.system('rmdir /S /Q "' + os.getcwd() + dir + '"')
        time.sleep(1)

def createFolderStructure():
    
    # Folder Structure

    # Vorkurs Mathematik
    # - Skript
    #   - Woche 1
    #   ...
    #   - Woche 4
    # - Kompakt
    #   - Woche 1
    #   ...
    #   - Woche 4
    # - Aufgaben
    #   - Woche 1
    #     - Aufgabe
    #     - Ergebnis
    #     - Lösung
    #   ...
    #   - Woche 4
    #     ...

    def createFolder(dir):
        dir = os.getcwd() + dir
        if not os.path.exists(dir):
            os.makedirs(dir)

    def createWeeks(baseDir):
        for i in range(4):
            createFolder(baseDir + "/Woche " + str(i + 1))

    def aufgabenFolder(baseDir):
        for i in range(4):
            createFolder(baseDir + "/Woche " + str(i + 1) + "/Aufgabe")
            createFolder(baseDir + "/Woche " + str(i + 1) + "/Ergebnis")
            createFolder(baseDir + "/Woche " + str(i + 1) + "/Lösung")
           
    deleteFolder("/DownloadTemp")
    createFolder("/DownloadTemp")

    if os.path.exists(os.getcwd() + "/Vorkurs Mathematik/"):
        overwrite = input("Folder allready exists!\n Continuing will delete all data in the Folder \"/Vorkurs Mathematik\".\n To Continue (Y), to Cancel (N): ")
        print()

        if overwrite.strip().lower() == "n":
            sys.exit(0)
            
        deleteFolder("/Vorkurs Mathematik")
        
    createFolder("/Vorkurs Mathematik/Info")
    createWeeks("/Vorkurs Mathematik/Skript")
    createWeeks("/Vorkurs Mathematik/Kompakt")
    aufgabenFolder("/Vorkurs Mathematik/Aufgaben")

    return

def crawlDay(driver, dayName, href):

    print("Crawling now:", dayName)

    dayNumber = int(dayName[4:6])
    weekNumber = ((dayNumber - 1) // 5) + 1
    
    def moveToFolder(baseDir, subDir = "", addweek = True):

        if addweek:
            dir = os.getcwd() + "/Vorkurs Mathematik/" + baseDir + "/Woche " + str(weekNumber) + subDir + "/"
        else:
            dir = os.getcwd() + "/Vorkurs Mathematik/" + baseDir + subDir + "/"

        files = []
        while not files:
            files = glob.glob(os.getcwd() + "/DownloadTemp/*.pdf")
            time.sleep(0.1)

        for file in files:
            newFileName = dir + str(dayNumber) + ".  " + os.path.split(file)[1] # path split gets filename + extension
            if not os.path.exists(newFileName):
                os.rename(file, newFileName)
            else:
                os.remove(file)

    #open tab ?

    # Load page 
    driver.get(href)

    pdfs = []
    # get all links with goto.php in href
    for element in driver.find_elements_by_css_selector("div.ilContainerItemsContainer a"):
        if 'goto.php' in element.get_attribute('href') and element.text.strip() != "":
            pdfs.append((element.text.strip().lower(), element.get_attribute('href')))

    for name, link in pdfs:
        if name.startswith("skript"):
            driver.get(link)
            moveToFolder("Skript")
        elif name.endswith("kompakt"):
            driver.get(link)
            moveToFolder("Kompakt")
        elif name.startswith("vkm"):
            if "info" in name:
                driver.get(link)
                moveToFolder("Info", addweek = False)
            if name.endswith("erg"):
                driver.get(link)
                moveToFolder("Aufgaben", "/Ergebnis")
            elif name.endswith("lsg"):
                driver.get(link)
                moveToFolder("Aufgaben", "/Lösung")
            else:
                driver.get(link)
                moveToFolder("Aufgaben", "/Aufgabe")

    # check the text of the link
    # - starts with "Script"
    # - ends with "kompakt"
    # - starts with "VKM2020_Ag"
    #   - ends with "Erg"
    #   - ends with "Lsg"

    # save the pdf to that folder
    
    # close the tab ?
    return

createFolderStructure()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('prefs', {
    "download.default_directory": os.getcwd() + "\\DownloadTemp\\", #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})
#options.add_argument("--disable-gpu")
#options.add_argument("--headless")

try:
    driver = webdriver.Chrome(options=options)
except :
    print("Webdriver not found, please check the chromedriver.exe, the Version of the driver and your Google Chrome")
    time.sleep(3)
    sys.exit(0)

login(driver)

# expand Weeks to load day data
for element in driver.find_elements_by_class_name('ilContainerBlockHeaderCollapsed'):
    driver.execute_script('arguments[0].click();', element)
  
time.sleep(1)
  
days = []
for element in driver.find_elements_by_partial_link_text('Tag '):
    days.append((element.text, element.get_attribute('href')))

for dayName, href in days:
    crawlDay(driver, dayName, href)

deleteFolder("/DownloadTemp")
print("\nDone!")
driver.close()