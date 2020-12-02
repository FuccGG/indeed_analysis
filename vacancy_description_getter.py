import urllib.parse
import requests
import time
import pandas as pd
import csv
from bs4 import BeautifulSoup
from main import get_content
# 'https://www.indeed.com/rc/clk?jk=083cf3ac35e2f5d7&fccid=a84e2d6d6acdfd79&vjs=3'


def get_link_list():
    link_list = []
    with open("vacancy_links.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            link_list.append(dict(row)['link'])
    return link_list


def get_desc(link):
    time.sleep(5)
    soup = BeautifulSoup(get_content(link), 'html.parser')
    return soup.find('div', class_='jobsearch-jobDescriptionText').text


def to_txt(desc):
    file1 = open("data.txt", "a")
    file1.write(desc)
    file1.close()


link_list = get_link_list()
for link in link_list:
    desc = get_desc(link)
    try:
        to_txt(desc)
    except:
        print(link)
