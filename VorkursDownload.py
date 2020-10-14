import os
import time
import glob
from Util import *

username = ""
password = ""

FolderToSaveTo = r"C:\Users"
ErrorLogFilePath = r"C:\Users\AutoDownloadError.log"

initUtil(FolderToSaveTo, ErrorLogFilePath)

WebsiteToCrawl = "https://ilias.studium.kit.edu/goto.php?target=crs_1235442&client_id=produktiv"
WebsiteToLogin = "https://ilias.studium.kit.edu/login.php?cmd=force_login&lang=de"

def beforeStart():
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

        def createWeeks(baseDir):
            for i in range(4):
                createFolder(baseDir + "/Woche " + str(i + 1))

        def aufgabenFolder(baseDir):
            for i in range(4):
                createFolder(baseDir + "/Woche " + str(i + 1) + "/Aufgabe")
                createFolder(baseDir + "/Woche " + str(i + 1) + "/Ergebnis")
                createFolder(baseDir + "/Woche " + str(i + 1) + "/Lösung")
           
        createFolder("/DownloadTemp")

        createFolder("/Vorkurs Mathematik/Info")
        createWeeks("/Vorkurs Mathematik/Skript")
        createWeeks("/Vorkurs Mathematik/Kompakt")
        aufgabenFolder("/Vorkurs Mathematik/Aufgaben")

    if os.path.exists(ErrorLogFilePath):
        os.remove(ErrorLogFilePath)

    deleteFolder("/DownloadTemp")
    deleteFolder("/Vorkurs Mathematik")
        
    createFolderStructure()

def beforeCrawl(driver):
    for element in driver.find_elements_by_class_name('ilContainerBlockHeaderCollapsed'):
        driver.execute_script('arguments[0].click();', element)
  
    time.sleep(1)

def getLinksToCrawl(driver) -> (str, str):
    
    days = []
    for element in driver.find_elements_by_partial_link_text('Tag '):
        days.append((element.text, element.get_attribute('href')))

    return days
 
def crawl(driver, text: str, link: str):

    if not text.startswith("Tag"):
        return

    print("Crawling now:", text)

    dayNumber = int(text[4:6])
    weekNumber = ((dayNumber - 1) // 5) + 1
    
    def moveToFolder(baseDir, subDir = "", addweek = True):

        if addweek:
            dir = FolderToSaveTo + "/Vorkurs Mathematik/" + baseDir + "/Woche " + str(weekNumber) + subDir + "/"
        else:
            dir = FolderToSaveTo + "/Vorkurs Mathematik/" + baseDir + subDir + "/"

        files = []
        while not files:
            files = glob.glob(FolderToSaveTo + "/DownloadTemp/*.pdf")
            time.sleep(0.1)

        for file in files:
            newFileName = dir + str(dayNumber) + ".  " + os.path.split(file)[1] # path split gets filename + extension
            if not os.path.exists(newFileName):
                os.rename(file, newFileName)
            else:
                os.remove(file)

    pdfs = []
    # get all links with goto.php in link
    for element in driver.find_elements_by_css_selector("div.ilContainerItemsContainer a"):
        if 'goto.php' in element.get_attribute('href') and element.text.strip():
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

    return

def cleanup(driver):
    deleteFolder("/DownloadTemp")
    print("\nDone!")
    driver.close()