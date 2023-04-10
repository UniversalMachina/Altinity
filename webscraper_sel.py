from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import os


"""
This is a college project I made using the chrome webdriver and selenium to webscrape stock footage from a website. 
The website has recently added anti-botting features, but this is some of the general logic I used to webscrape thousands 
of bits of media for a media editing project. 
"""

Searchwords=["Trees","Cars"]


def filedownloader(subpath="E:\\", indices=0):
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': subpath}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # driver = webdriver.Chrome(Service=("C:\\Users\\Eric\\Downloads\\chromedriver_win32\\chromedriver.exe"),
        #                           options=chrome_options)

        def getDownLoadedFileName(waitTime):
            driver.execute_script("window.open()")
            # switch to new tab
            driver.switch_to.window(driver.window_handles[-1])
            # navigate to chrome downloads
            driver.get('chrome://downloads')
            # define the endTime
            endTime = time.time() + waitTime
            while True:
                try:
                    # get downloaded percentage
                    downloadPercentage = driver.execute_script(
                        "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
                    # check if downloadPercentage is 100 (otherwise the script will keep waiting)
                    if downloadPercentage == 100:
                        # return the file name once the download is completed
                        return driver.execute_script(
                            "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
                except:
                    pass
                time.sleep(1)
                if time.time() > endTime:
                    break

        driver.get('https://pixabay.com/videos/')
        # time.sleep(2)
        launch = True
        while launch == True:
            try:
                searchbox = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                    driver.find_element("xpath", '/html/body/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/form/input')))
                searchbox.send_keys(Searchwords[i])
                launch = False
            except:
                pass

        time.sleep(2)
        searchbutton = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                driver.find_element("xpath", '/html/body/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/form/button/span')))
        searchbutton.click()
        for x in range(10):
            time.sleep(2)
            # video = driver.find_element("xpath",'//*[@id="content"]/div/div[3]/div/div[2]/div[1]/div/div/div/a/div/img')
            # video.click()
            driver.execute_script("window.scrollTo(0, 200)")
            try:
                video = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element("xpath",
                                                                                                       '/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div[' + str(
                                                                                                           x + 1) + ']/div/div/div/a/div/img')))
                video.location_once_scrolled_into_view
                video.click()
            except:
                pass
            try:
                download = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                    driver.find_element("xpath", '/html/body/div[1]/div[2]/div[2]/div[2]/div[4]/span')))
                download.click()
                confirmdownload = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                    driver.find_element("xpath", '/html/body/div[1]/div[2]/div[2]/div[2]/div[4]/div/a[2]')))
                confirmdownload.click()
                latestDownloadedFileName = getDownLoadedFileName(180)  # waiting 3 minutes to complete the download
                print(latestDownloadedFileName)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.back()
            except:
                driver.switch_to.window(driver.window_handles[0])
                driver.back()

            try:
                indices = indices + 1
                print(indices)
                os.rename(os.path.join(subpath, latestDownloadedFileName), os.path.join(subpath, str(indices) + ".mp4"))
            except FileExistsError:
                os.remove(os.path.join(subpath, str(indices) + ".mp4"))
                os.rename(os.path.join(subpath, latestDownloadedFileName), os.path.join(subpath, str(indices) + ".mp4"))
            except FileNotFoundError:
                print("file missing")
                indices = indices - 1
            except:
                indices -= 1
                # print("testing")
        return indices

if Searchwords:
    for i in range(len(Searchwords)):
        indices1 = filedownloader()