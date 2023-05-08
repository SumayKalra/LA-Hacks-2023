from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import classdata as cd
import time
import re

'''remeber for class data its hard coded in chem'''
#function scrapes data
def scrapping_data(input_class, input_term):
    #user inputs
    class_data = input_class.split(" ")
    class_name = class_data[0]
    class_num = class_data[1]

    # Start a new Chrome browser instance and navigate to the UCSD Schedule of Classes website
    driver = webdriver.Chrome()
    driver.get("https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudent.htm")

    #Term drop down menu
    term_menu = Select(driver.find_element(By.ID,"selectedTerm"))
    term_menu.select_by_value(input_term)
    time.sleep(0.5) #gives time for processing

    #Subject drop down menu
    subject_menu = Select(driver.find_element(By.ID,"selectedSubjects"))
    subject_menu.select_by_value(class_name)

    #click search button
    search_button_main = driver.find_element(By.ID, "socFacSubmit")
    search_button_main.click()

    #Extracting table data for subject
    index_lst =[]
    class_data_lst = []
    class_table  = driver.find_element(By.CLASS_NAME,"tbrdr")
    rows = class_table.find_elements(By.TAG_NAME, "tr")
    page_num = 1
    for row in rows:
        if class_num in row.text and rows.index(row) != 1:
            index_lst.append(rows.index(row))
    if len(index_lst) == 0:
        index_lst, rows, page_num = goes_to_next_page(class_num, index_lst, driver, page_num)
    

    class_table  = driver.find_element(By.CLASS_NAME,"tbrdr")
    rows = class_table.find_elements(By.TAG_NAME, "tr")

    index_lst[len(index_lst)-1] = index_lst[len(index_lst)-1] + 1
    first_run = True
    next_index = cd.CHEM.index(input_class) + 1
    index_lst = find_next_class_same_page(rows, index_lst, input_class,first_run, next_index)
    for i in range(index_lst[0],index_lst[len(index_lst)-1]):
        class_data_lst.append(rows[i].text)

    #placing and matching data into a lecture list and disc list
    lec_index = []
    disc_index = []
    print(index_lst)
    for i in class_data_lst:
        if "LE" in i:
            pattern = r"(MWF|TuTh|M|Tu|W|Th|F|MW)(,?\s*)(\d{1,2}:\d{2}[ap])-*(\d{1,2}:\d{2}[ap]*)"
            matches = re.findall(pattern, i)
            if len(matches) != 0:
                lec_index.append(matches[0])
        if "DI" in i or "LA" in i:
            disc_index.append(class_data_lst.index(i))
    
    lists_disc_index= []
    count = 0
    for i in disc_index:
        if disc_index.index(i) is len(disc_index)-1:
            lists_disc_index.append(disc_index[count:disc_index.index(i)+1])
        elif i + 1 != disc_index[disc_index.index(i) +1]:
            lists_disc_index.append(disc_index[count:disc_index.index(i)+1])
            count = disc_index.index(i) + 1
    for i in range(len(lists_disc_index)):
        for j in range(len(lists_disc_index[i])):
            pattern = r"(MWF|TuTh|M|Tu|W|Th|F)(,?\s*)(\d{1,2}:\d{2}[ap])-*(\d{1,2}:\d{2}[ap]*)"
            matches = re.findall(pattern, class_data_lst[lists_disc_index[i][j]])
            if len(matches) != 0:
                lists_disc_index[i][j] = matches[0]
  
    #formating into list of list format
    for i, tup in enumerate(lec_index):
        lec_index[i] = tuple(val for val in tup if val != " ")
    lec_index = [list(t) for t in lec_index]

    for element in lists_disc_index:
        for name in element:
            if not isinstance(name, tuple):
                lists_disc_index.remove(element)
    
    for tuples in lists_disc_index:
        tuples[:] = [[item for item in tpl if item != ' '] for tpl in tuples]
    
    #ouput for testing
    print(input_class)
    print(lec_index)
    print(lists_disc_index)
    

#finds the index of the next class
def find_next_class_same_page(rows, index_lst, input_class, first_run, next_index):
    if first_run:
        next_index = cd.CHEM.index(input_class) + 1
    else:
        next_index += 1
    class_data = cd.CHEM[next_index]
    class_data = class_data.split(" ")
    class_num = class_data[1]
    checker = False
    first_run = False
    if class_num in cd.CHEM_edge_cases:
        class_num = cd.CHEM_edge_cases[class_num]
    for row in rows:        
        if class_num in row.text:
            index_lst.append(rows.index(row))
            checker = True
            break
    if checker is False:
        return find_next_class_same_page(rows, index_lst, input_class, first_run, next_index)
    elif checker is True:
        return index_lst
        


#checks next page
def goes_to_next_page(class_num, index_lst, driver, page_num):
    page_button_xpath = '//*[@id="socDisplayCVO"]/div[2]/table/tbody/tr/td[3]/a[' + str(page_num) + ']'
    page_button = driver.find_element(By.XPATH, page_button_xpath)
    page_button.click()
    class_table  = driver.find_element(By.CLASS_NAME,"tbrdr")
    rows = class_table.find_elements(By.TAG_NAME, "tr")
    if class_num in cd.CHEM_edge_cases:
        class_num = cd.CHEM_edge_cases[class_num]
    for row in rows:
        if class_num in row.text:
            index_lst.append(rows.index(row))
    if len(index_lst) == 0:
        page_num += 1
        goes_to_next_page(class_num, index_lst, driver, page_num)
    else:
        return index_lst, rows, page_num

'''
def checks_next_page(class_num, driver,page_num):
    checker = False
    page_num += 1
    page_button_xpath = '//*[@id="socDisplayCVO"]/div[2]/table/tbody/tr/td[3]/a[' + str(page_num) + ']'
    page_button = driver.find_element(By.XPATH, page_button_xpath)
    page_button.click()
    class_table  = driver.find_element(By.CLASS_NAME,"tbrdr")
    rows = class_table.find_elements(By.TAG_NAME, "tr")
    if class_num in cd.CHEM_edge_cases:
        class_num = cd.CHEM_edge_cases[class_num]
    for row in rows:
        if class_num in row.text:
            checker = True
            break
    return checker
    '''