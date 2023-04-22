import requests
from bs4 import BeautifulSoup
import classes as cls

def url_creator(cls_name):
    space = 0
    for i in cls_name:
        if i == " ":
            space = space + 1
    for i in cls_name:
        if i == " ":
            new_cls_name = cls_name[0:cls_name.index(i)]
            break
    if space == 0:
        pass
    #print(new_cls_name)
    #response = requests.get(url)
    #soup = BeautifulSoup(response.content, 'html.parser')

