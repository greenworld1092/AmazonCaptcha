
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


chrome_driver = None
csv_file = None


def chrome_available():
    try:
        chrome_driver.title
        return True
    except:
        return False


def find_element(key, value):
    while True:
        try:
            return chrome_driver.find_element(
                key, value)
        except:
            if chrome_available() == False:
                return None
        time.sleep(1)


def find_element_children(parent, key, value):
    while True:
        try:
            return parent.find_element(
                key, value)
        except:
            if chrome_available() == False:
                return None
        time.sleep(1)


def init_chrome_driver():
    chrome_driver = webdriver.Chrome(executable_path=r"chromedriver.exe")

    chrome_driver.get(
        "https://cases.ra.kroll.com/StonewayCapital/Home-DocketInfo")
    
    return chrome_driver


def writeToCSV(cA, cB, cC):
    csv_file.writerow([cA, cB, cC])


def wait_for_load():
    while True:
        load = find_element("id", "load_results-table")
        if load == None:
            return
        if load.get_attribute("style") == "":
            continue
        return


def extract():
    while True:
        wait_for_load()
        results = find_element("id", "results-table")
        if results == None:
            return
        tbody = results.find_element(By.TAG_NAME, "tbody")
        res = tbody.find_elements(By.TAG_NAME, "tr")
        for ele in res:
            classname = ele.get_attribute("class")
            if "ui-widget-content" in classname:
                tds = ele.find_elements(By.TAG_NAME, "td")

                o_docket = ""
                try:
                    o_docket = tds[0].find_element(
                        By.TAG_NAME, "span").get_attribute('innerText')
                except:
                    pass
                o_name = tds[1].find_element(
                    By.TAG_NAME, "span").find_element(By.TAG_NAME, "p").get_attribute('innerText')
                o_date = tds[2].find_element(
                    By.TAG_NAME, "span").get_attribute('innerText')

                writeToCSV(o_docket, o_name, o_date)
        pagenum = find_element("id", "pagenum").get_attribute("value")
        total_pages = find_element(
            "id", "p-total-pages").get_attribute('innerText')
        if int(pagenum) == int(total_pages):
            break
        next_page = find_element("id", "p-next-page")
        chrome_driver.execute_script(
            "arguments[0].click();", next_page)
        time.sleep(1)


def main():
    global chrome_driver
    global csv_file

    chrome_driver = init_chrome_driver()

    file = open("output.csv", "w", encoding='utf-8', newline='')
    csv_file = csv.writer(file)

    extract()

    file.close()


main()
