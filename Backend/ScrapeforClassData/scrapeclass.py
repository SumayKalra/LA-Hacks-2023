from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
import re


def scrapping_data_classes():
    driver = webdriver.Chrome()
    driver.get("https://math.ucsd.edu/students/planned-course-offerings")
    list_of_classes_num = []
    list_of_classes_name = []
    driver.implicitly_wait(10)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")
    anchor_tags = table.find_all('a')
    class_names = table.find_all('td', class_='text-left')
    for i in class_names:
        i = re.sub(r'\s+(?!\S)', '', i.text.strip())
        list_of_classes_name.append(i)
    for i in anchor_tags:
        i = re.sub(r'\s+(?!\S)', '', i.text.strip())
        list_of_classes_num.append(i)
    list_of_classes_num = [item for item in list_of_classes_num if any(char.isdigit() for char in item)]
    print(list_of_classes_num)
    print(list_of_classes_name)
    #CHEM 1
    #//*[@id="undergrad-table"]/tbody/tr[1]/td[1]/a
    #//*[@id="undergrad-table"]/tbody/tr[1]/td[2]

    #CHEM 4
    #//*[@id="undergrad-table"]/tbody/tr[2]/td[1]/a
    #//*[@id="undergrad-table"]/tbody/tr[2]/td[2]

    #CHEM 6A
    #//*[@id="undergrad-table"]/tbody/tr[3]/td[1]/a

    #//*[@id="undergrad-table"]/tbody/tr[64]/td[1]/a