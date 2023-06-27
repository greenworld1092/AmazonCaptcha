import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from twocaptcha import TwoCaptcha
import sys

chrome_driver = None

def chrome_available():
    try:
        chrome_driver.title
        return True
    except:
        return False

def init_chrome_driver():
    chrome_driver = webdriver.Chrome(executable_path=r"chromedriver.exe")

    chrome_driver.get(
        "https://cases.ra.kroll.com/StonewayCapital/Home-DocketInfo")
    
    return chrome_driver
def extract():
    solver = TwoCaptcha('90ac4cda3f3884430dd769e81a811a82')

    sitekey = input("Please enter sitekey\n")
    iv = input("Please enter iv\n")
    context = input("Please enter context\n")

    try:
        result = solver.amazon_waf(
            sitekey=sitekey,
            iv=iv,
            context=context,
            url='https://cases.ra.kroll.com/StonewayCapital/Home-DocketInfo',
        )

    except Exception as e:
        sys.exit(e)

    else:
        sys.exit('result: ' + str(result))
    return True

def main():
    global chrome_driver

    chrome_driver = init_chrome_driver()

    extract()
main()