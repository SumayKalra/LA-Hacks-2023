from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
import classes as cls

def url_creator(cls_name):
    # get subject
    lsi = cls_name.rfind(" ")
    cls_sub = cls_name[:lsi]
    cls_num = cls_name[lsi:]
    #activate driver
    driver = webdriver.Chrome()
    driver.get("https://sa.ucla.edu/ro/Public/SOC")  

    #term scorller
    dropdown = Select(driver.find_element("optSelectTerm")) 
    dropdown.select_by_value("23S")
    
    #search bar
    search_bar = driver.find_element("iwe-autocomplete-35")
    search_bar.send_keys(cls_sub)
    search_bar.submit()

    # pressing button 
    button = driver.find_element("btn_go")
    button.click() 

    #Expand all button
    button = driver.find_element("expandAll")
    button.click()

    #new urls
    new_url = driver.current_url
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, "html.parser")

    #scraping 
    element = soup.find("div", class_="timeColumn", id  = "187096200_"  + cls_name + "00" + cls_num + "-time_data") 
    data = element.text
    print(data)

