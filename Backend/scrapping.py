from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import classdata as cd
import time
import re

count= 0
#function scrapes data
'page number issue'
'scrape through next page'
def scrapping_data(input_class, input_term):
    #user inputs
    class_data = input_class.split(" ",1)
    class_name = class_data[0]
    class_num =  cd.CHEM_name[cd.CHEM_num.index(input_class)]

    # Start a new Chrome browser instance and navigate to the UCSD Schedule of Classes website
    time.sleep(1)
    driver = webdriver.Chrome()
    time.sleep(1)
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
    total_pages = driver.find_element(By.XPATH, "//td[contains(text(),'Page')]")
    total_pages = total_pages.text
    total_pages_num = 1
    for i in total_pages:
        try:
            if int(i) > total_pages_num:
                total_pages_num = i
        except TypeError:
            pass
        except ValueError:
            pass

    for row in rows:
        if class_num in row.text and rows.index(row) != 1: #and row.text[row.text.index(class_num) -1] == " " :
            index_lst.append(rows.index(row))
    if len(index_lst) == 0:
        index_lst, page_num = goes_to_next_page(class_num, index_lst, driver, page_num, total_pages_num)
    if len(index_lst) == 0:
        print(input_class)
        print("No class found for that quarter")
        print()
        driver.quit()
        return "nothing"
    class_table  = driver.find_element(By.CLASS_NAME,"tbrdr")
    rows = class_table.find_elements(By.TAG_NAME, "tr")
    #print(index_lst)
    if len(index_lst) > 1:
        index_lst[len(index_lst)-1] = index_lst[len(index_lst)-1] + 1
    first_run = True
    next_index = cd.CHEM_num.index(input_class) + 1
    end_page = True
    index_lst, lec_indexp2, disc_indexp2 = find_next_class_same_page(rows, index_lst, input_class,first_run,  next_index,class_table, driver ,page_num, total_pages_num, end_page)
    class_table  = driver.find_element(By.CLASS_NAME,"tbrdr")
    rows = class_table.find_elements(By.TAG_NAME, "tr")

  
    for i in range(index_lst[0],index_lst[len(index_lst)-1]):
        class_data_lst.append(rows[i].text)

    class_table  = driver.find_element(By.CLASS_NAME,"tbrdr")
    rows = class_table.find_elements(By.TAG_NAME, "tr")
    #placing and matching data into a lecture list and disc list
    lec_index = []
    disc_index = []
    for i in class_data_lst:
        if "LE" in i:
            pattern = r"(MWF|TuTh|M|Tu|W|Th|F|MW)(,?\s*)(\d{1,2}:\d{2}[ap])-*(\d{1,2}:\d{2}[ap]*)"
            matches = re.findall(pattern, i)
            if len(matches) != 0 and len(matches[0]) == 4:
                lec_index.append(matches[0])
        if "DI" in i or "LA" in i:
            disc_index.append(class_data_lst.index(i))
        
    lists_disc_index= []
    count2 = 0
    for i in disc_index:
        if disc_index.index(i) is len(disc_index)-1:
            lists_disc_index.append(disc_index[count2:disc_index.index(i)+1])
        elif i + 1 != disc_index[disc_index.index(i) +1]:
            lists_disc_index.append(disc_index[count2:disc_index.index(i)+1])
            count2 = disc_index.index(i) + 1
    for i in range(len(lists_disc_index)):
        for j in range(len(lists_disc_index[i])):
            pattern = r"(MWF|TuTh|M|Tu|W|Th|F)(,?\s*)(\d{1,2}:\d{2}[ap])-*(\d{1,2}:\d{2}[ap]*)"
            matches = re.findall(pattern, class_data_lst[lists_disc_index[i][j]])
            if len(matches) != 0:
                lists_disc_index[i][j] = matches[0]
  
    '''
    if len(lec_index) == 0:
        for i in class_data_lst:
            if "SE" in i:
                pattern = r"(MWF|TuTh|M|Tu|W|Th|F|MW)(,?\s*)(\d{1,2}:\d{2}[ap])-*(\d{1,2}:\d{2}[ap]*)"
                matches = re.findall(pattern, i)
                if len(matches) != 0 and len(matches[0]) == 4:
                    lec_index.append(matches[0])
    '''
    #formating into list of list format
    lec_index = [[item for item in sublist if item.strip()] for sublist in lec_index]
    for element in lists_disc_index:
        for name in element:
            if not isinstance(name, tuple):
                lists_disc_index.remove(element)
    
    try:
        for tuples in lists_disc_index:
            tuples[:] = [[item for item in tpl if item != ' '] for tpl in tuples]
    except TypeError:
        lists_disc_index = []
    
    disc_index = lists_disc_index


    if len(lec_indexp2) > 0:
        for i in lec_indexp2:
            lec_index.append(i)
    if len(disc_indexp2) > 0:
        for i in disc_indexp2:
            disc_index.append(i)
    #ouput for testing
    print(input_class)
    print(lec_index)
    print(disc_index)    
    print()
    driver.quit()
    return "nothing"

#finds the index of the next class
def find_next_class_same_page(rows, index_lst, input_class, first_run, next_index,class_table, driver ,page_num, total_pages_num, end_page):
    empty_lst =[]
    if first_run:
        next_index = cd.CHEM_num.index(input_class) + 1

    else:
        next_index += 1
    class_num = cd.CHEM_name[next_index]
    checker = False
    if first_run:
        end_page = True
    for row in rows:
        if class_num in row.text and rows.index(row) != 1 and rows.index(row) != 0 and rows.index(row) > index_lst[0]:
            index_lst.append(rows.index(row))
            checker = True
            break
    if first_run:
        for i in cd.CHEM_name[next_index:]:
            for j in rows[index_lst[0]+ 1:]:
                if i in j.text:
                    end_page = False       
                    break     
            if end_page == False:
                break
    first_run = False
    if end_page is True and checker is False:
        index_lst.append(len(rows))
        class_num = cd.CHEM_name[cd.CHEM_num.index(input_class)]
        next_index -= 1
        lec_indexp2, disc_indexp2 = check_next_pages_func(driver, class_num, page_num, total_pages_num, input_class, first_run, next_index)
        return index_lst, lec_indexp2,disc_indexp2
    elif checker is False:
        return find_next_class_same_page(rows, index_lst, input_class, first_run,  next_index,class_table, driver ,page_num, total_pages_num, end_page)
    elif checker is True:
        return index_lst, empty_lst, empty_lst
    


#checks next page
def goes_to_next_page(class_num, index_lst, driver, page_num, total_page_num):
    new_page = int(total_page_num) -1
    if page_num == new_page and int(total_page_num) == 7:
        return index_lst, page_num
    page_num = get_proper_page(total_page_num, page_num)
    page_button_xpath = '//*[@id="socDisplayCVO"]/div[2]/table/tbody/tr/td[3]/a[' + str(page_num) + ']'
    page_button = driver.find_element(By.XPATH, page_button_xpath)
    page_button.click()
    class_table  = driver.find_element(By.CLASS_NAME,"tbrdr")
    rows = class_table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        if class_num in row.text:
            index_lst.append(rows.index(row))
    if len(index_lst) == 0:
        if(page_num == 1):
                page_num = page_num + 1
        return goes_to_next_page(class_num, index_lst, driver, page_num, total_page_num)
    else:
        return index_lst, page_num
    
def get_proper_page(total_page_num, page_num):
    global count
    total_page_num = int(total_page_num)
    if page_num > total_page_num:
        return page_num
    if total_page_num <= 5:
        if page_num == 1:
            return page_num 
        elif page_num == 2:
            return page_num + 1
        elif page_num == 3:
            return page_num + 1
        elif page_num == 4:
            return page_num +1
    if total_page_num == 6:
        if page_num == 1:
            return page_num
        if page_num >= 2 and page_num < 6:
            return page_num + 1
    if(total_page_num == 7):
        if page_num == 1:
            return page_num
        elif page_num == 2:
            return page_num + 1
        elif page_num == 3 and count == 0:
            count += 1
            return page_num
        elif page_num == 3 and count == 1:
            return page_num + 1
        elif page_num == 4:
            return page_num + 1
        elif page_num == 5:
            return page_num + 1
        elif page_num == 5:
            return page_num + 1

def get_proper_page2(total_pages_num, page_num,first_run):
    total_pages_num = int(total_pages_num)
    if total_pages_num == 7:
        if page_num == 1:
            return page_num + 2
        elif page_num == 2:
            return page_num + 1
        elif page_num == 3 and first_run is True:
            return page_num
        elif page_num == 3 and first_run is False:
            return page_num + 1
        elif page_num == 4:
            return page_num + 1
        elif page_num == 5:
            return page_num + 1

def check_next_pages_func(driver, class_num, page_num, total_pages_num, input_class, first_run, next_index):
    #print("check_next_pages_func")
    checker = False
    end_page = True
    add_index_lst = []
    current_url = driver.current_url
    page_num = get_proper_page2(total_pages_num, page_num,first_run)
    page_button_xpath = '//*[@id="socDisplayCVO"]/div[2]/table/tbody/tr/td[3]/a[' + str(page_num) + ']'
    page_button = driver.find_element(By.XPATH, page_button_xpath)
    page_button.click()
    class_table  = driver.find_element(By.CLASS_NAME,"tbrdr")
    rows = class_table.find_elements(By.TAG_NAME, "tr")
    lec_index = []
    disc_index = []
    for row in rows:
        if class_num in row.text:
            checker = True
            add_index_lst.append(rows.index(row))
    if checker is True:
        add_index_lst = find_next_class_same_page(rows, add_index_lst, input_class, first_run, next_index,class_table, driver ,page_num, total_pages_num, end_page)
        add_index_lst = add_index_lst[0]
        class_data_lst = []
        for i in range(add_index_lst[0],add_index_lst[len(add_index_lst)-1]):
            class_data_lst.append(rows[i].text)
        for i in class_data_lst:
            if "LE" in i:
                pattern = r"(MWF|TuTh|M|Tu|W|Th|F|MW)(,?\s*)(\d{1,2}:\d{2}[ap])-*(\d{1,2}:\d{2}[ap]*)"
                matches = re.findall(pattern, i)
                if len(matches) != 0 and len(matches[0]) == 4:
                    lec_index.append(matches[0])
            if "DI" in i or "LA" in i:
                disc_index.append(class_data_lst.index(i))

        if len(lec_index) == 0:
            for i in class_data_lst:
                if "SE" in i:
                    pattern = r"(MWF|TuTh|M|Tu|W|Th|F|MW)(,?\s*)(\d{1,2}:\d{2}[ap])-*(\d{1,2}:\d{2}[ap]*)"
                    matches = re.findall(pattern, i)
                    if len(matches) != 0 and len(matches[0]) == 4:
                        lec_index.append(matches[0])
        lists_disc_index= []
        count2 = 0
        for i in disc_index:
            if disc_index.index(i) is len(disc_index)-1:
                lists_disc_index.append(disc_index[count2:disc_index.index(i)+1])
            elif i + 1 != disc_index[disc_index.index(i) +1]:
                lists_disc_index.append(disc_index[count2:disc_index.index(i)+1])
                count2 = disc_index.index(i) + 1
        for i in range(len(lists_disc_index)):
            for j in range(len(lists_disc_index[i])):
                pattern = r"(MWF|TuTh|M|Tu|W|Th|F)(,?\s*)(\d{1,2}:\d{2}[ap])-*(\d{1,2}:\d{2}[ap]*)"
                matches = re.findall(pattern, class_data_lst[lists_disc_index[i][j]])
                if len(matches) != 0:
                    lists_disc_index[i][j] = matches[0]

        #formating into list of list format
        lec_index = [[item for item in sublist if item.strip()] for sublist in lec_index]
        for element in lists_disc_index:
            for name in element:
                if not isinstance(name, tuple):
                    lists_disc_index.remove(element)
        
        for tuples in lists_disc_index:
            tuples[:] = [[item for item in tpl if item != ' '] for tpl in tuples]
        
        disc_index = lists_disc_index
        
    
        #formating into list of list format
        lec_index = [[item for item in sublist if item.strip()] for sublist in lec_index]
        '''
        disc_index =[[item for item in sublist if item.strip()] for sublist in disc_index]
        '''
        driver.get(current_url)
        return lec_index, disc_index
    else:
        driver.get(current_url)
        return lec_index, disc_index

