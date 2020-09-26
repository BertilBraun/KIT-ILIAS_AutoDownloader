# KIT-ILIAS AutoDownloader
 A Simple tool to download Study files 
 
___

## How it Works

  * The Program opens a virtual Browser Window and emulates a user.
  * It first has to login using the **necessary provided Credentials** to get access to the downloads page.
  * Then it crawls through every day, dowloading every PDF file from that day.
  * Afterwards the files are sorted into the folder structure as seen above in the 'Vorkurs Mathematik' folder.

___

## How to Use

 ### Simply download the 'dist' Folder and run the Program 'AutoDownload.exe'.
 To Verify: `0f1eed7b7309c3bb7858ebb08e950a8f` MD5 Checksum.
 
 You **need** to have the 'chromedriver.exe' in the same Folder and Google Chrome Version 85 installed.
 
 To find out which version of Google Chrome you have installed:  * go to '...' in the upper right corner
  * then on 'Help' > 'About Google Chrome'.
  
 If you have another version of Google Chrome installed you can get the working driver from [here](https://chromedriver.chromium.org/downloads).
 
___

## How to Run

 If you want to run the Program yourself, you need to have.
 
  * Python
  * Google Chrome
  * The Driver (See Above)
  * Selenium `pip install selenium`
  
 Then simply run the Program with:
 `python AutoDownload.py`
  
___
