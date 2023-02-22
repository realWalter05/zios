from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from os.path import exists
import time

# Sets up selenium
chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome('./Chromedriver/chromedriver.exe', options=chrome_options)


def main():
    # Set data
    urls = ""
    driver.get(url)
    bus_titles = driver.findElement(By.className("table"));

    return links

if __name__ == "__main__":
    main()
