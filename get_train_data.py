from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from os.path import exists
import time
import sys
import json

# Sets up selenium
chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome('./Chromedriver/chromedriver.exe', options=chrome_options)

# Setting higher recursion depth
sys.setrecursionlimit(20000)

def get_item_data(item):
    departure = item.find_element(by=By.XPATH, value="./*[@class='departure']")
    name = item.find_element(by=By.XPATH, value="./*[@class='name']")
    fixed_codes = item.find_element(by=By.XPATH, value="./*[@class='fixed-codes']")
    
    item_data = {
       "name": name.get_attribute('innerHTML'),
       "departure": departure.get_attribute('innerHTML').split("</span>")[1].replace('\n', '').replace(" ", ""),
       "fixed_codes": fixed_codes.get_attribute('innerHTML').replace(r'\n', '').replace(" ", "")
    }
    return item_data

def get_items(url, links, json_file):
    # Open the page in selenium and find the bus titles
    driver.get(url)
    bus_titles = driver.find_elements(by=By.XPATH, value="//*[@style='color:#0000FF; display:inline']")

    for bus_title in bus_titles:
        # Waits until the title loads
        while bus_title.text == "":
            time.sleep(1)
        # Clicks on the bus title with js
        driver.execute_script("arguments[0].click();", bus_title)
        
        # Gets items
        items = driver.find_elements_by_class_name("item")
    
        # Gets item data
        items_data = []
        for item in items:
            # Waits until the items load
            while get_item_data(item)["name"] == "" and get_item_data(item)["departure"] == "":
                time.sleep(1)
            item_data = get_item_data(item)
            
             # Checking if the data is already indexed in new links or in old links
            if bus_title.text in links:
                if items_data in links[bus_title.text]:
                    continue    
            elif bus_title.text in json_file:
                if items_data in json_file[bus_title.text]:
                    continue  

            items_data.append(get_item_data(item))     

        items_data_sorted = sorted(items_data, key=lambda k: k['departure'])        
        # Appends data
        links[bus_title.text] = items_data_sorted
        if bus_title.text in links:
            links[bus_title.text] = [*links[bus_title.text], *items_data_sorted]
        print("Added " + bus_title.text)

    return links

def read_json(file):
    with open("links.json", "r", encoding="utf-8") as json_text:
        return json.load(json_text)

def write_json(file, links):
    # Writes the json
    with open(file, "w", encoding="utf-8") as p:
        json.dump(links, p)
      

def main():
    # Set data
    urls = [url for url in open("links.txt", "r").readlines()] if exists("links.txt") else ""
    json_file = read_json("links.json") if exists("links.json") else {} 
    links = {}

    # Get data for every url
    for main_url in urls:
        url_parts = main_url.split("?")
        url_times_days = [
         #   url_parts[0] + "?date=01.03.2022&time=00:00&" + url_parts[1],
            url_parts[0] + "?date=01.03.2022&time=9:00&" + url_parts[1],
          #  url_parts[0] + "?date=01.03.2022&time=19:00&" + url_parts[1]
        ]                                           
        
        for url in url_times_days:
            print(url)
            links = dict(list(links.items()) + list(get_items(url, links, json_file).items()))

    # Write combined json
    write_json("links.json", dict(list(json_file.items()) + list(links.items())))
    driver.close()
    driver.quit()
    print("Done")

if __name__ == "__main__":
    main()
