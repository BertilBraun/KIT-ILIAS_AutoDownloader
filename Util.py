import os
import time

FolderToSaveTo = r"C:\Users\Braun\OneDrive\Documents\Studium\Vorlesungen\Mathe\Semester 1"
ErrorLogFilePath = r"C:\Users\Braun\OneDrive\Desktop\AutoDownloadError.log"

def initUtil(folderToSaveTo, errorLogFilePath):
    global FolderToSaveTo, ErrorLogFilePath
    FolderToSaveTo = folderToSaveTo
    ErrorLogFilePath = errorLogFilePath

def logError(error):
    with open(ErrorLogFilePath, "a") as f:
        f.write(error)
    print(error)

def deleteFolder(dir):
    if os.path.exists(FolderToSaveTo + dir):
        os.system('rmdir /S /Q "' + FolderToSaveTo + dir + '"')
        time.sleep(1)

def createFolder(dir):
    dir = FolderToSaveTo + dir
    if not os.path.exists(dir):
        os.makedirs(dir)
