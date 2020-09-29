# KIT-ILIAS AutoDownloader
 A Simple tool to download Study files 
 
___

## How it Works

  * It first has to login using the **necessary provided Credentials** to get access to the downloads page.
  * The Program opens a virtual Browser Window and emulates a user.
    ![alt text](https://github.com/BertilBraun/KIT-ILIAS_AutoDownloader/raw/master/Images/Login.png "Login Example")
  * Then it crawls through every day, dowloading every PDF file from that day.
    ![alt text](https://github.com/BertilBraun/KIT-ILIAS_AutoDownloader/raw/master/Images/Downloading.png "Downloading Example")
  * Afterwards the files are sorted into the folder structure as seen above in the 'Vorkurs Mathematik' folder.
    ![alt text](https://github.com/BertilBraun/KIT-ILIAS_AutoDownloader/raw/master/Images/Done.png "Sorting Example")

___

## How to Use

 ### Simply download the 'dist' Folder and run the Program 'AutoDownload.exe'.
 To Verify: `8a0e8019191ac29a97e64b297a4c5513` MD5 Checksum.
 
 You **need** to have the 'chromedriver.exe' in the same Folder and Google Chrome Version 85 installed.
 
 To find out which version of Google Chrome you have installed:  * go to '...' in the upper right corner
  * then on 'Help' > 'About Google Chrome'.
  
 If you have another version of Google Chrome installed you can get the working driver from [here](https://chromedriver.chromium.org/downloads).
 
___
## Fix virus Scan Failed

1. From the Start screen, type regedit.exe, and then press Enter.

2. Go to the following registry key:
HKEY_LOCAL_MACHINE >SOFTWARE >Microsoft >Windows >CurrentVersion >Policies >Attachments

3. Double click on “ScanWithAntivirus” registry key and change its value to '1' which is by default '3'.

For the official Microsoft support Page click [here](https://support.microsoft.com/en-us/help/883260/information-about-the-attachment-manager-in-microsoft-windows).
This fix does not interfear with the blocking of actual Maleware.

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
