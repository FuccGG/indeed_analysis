import urllib.parse
import requests
import time
import pandas as pd
import csv
from bs4 import BeautifulSoup


def parse_indeed():
    main_url = 'https://www.indeed.com'
    vacancies_url = 'jobs?'
    q = 'programmer'  # Задаем интересующее название вакансии
    url = main_url + '/' + vacancies_url + urllib.parse.urlencode({'q': q})
    print(url)
    vacancy_links = parse_vacancy_links(url, [], main_url)
    link_list_to_csv(vacancy_links)
    # texts_sum = " "
    # print(vacancy_links)
    # for link in vacancy_links:
    #     content = get_content(link)
    #     print(content)
    #     texts_sum.join(get_content(link))
    # print(texts_sum)


def get_content(url):
    return requests.get(url).content.decode()


def parse_vacancy_links(url, link_list, domain):
    time.sleep(5)
    soup = BeautifulSoup(get_content(url), 'html.parser')
    results_col = soup.find('td', id='resultsCol')  # Сдираем всё с ячейки с превьюхами вакансий
    vacancy_plates = results_col.find_all('h2', class_='title')  # Сдираем все заголовки с ссылками на вакансии

    for plate in vacancy_plates:
        link_list.append(domain + plate.find('a').get('href'))  # Сдираем из заголовков ссылки

    print('Vacancies checked:' + str(len(link_list)))
    if soup.find('ul', class_='pagination-list').find_all('li')[-1].find('a') is None:  # Загон в рекурсию
        return link_list
    else:
        next_page = soup.find('ul', class_='pagination-list').find_all('li')[-1].find('a').get('href')
        return parse_vacancy_links(domain + next_page, link_list, domain)


def link_list_to_csv(link_list):
    counter = 0
    with open('vacancy_links.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "link"])
        for link in link_list:
            writer.writerow([str(int(counter)), link])
            counter = counter + 1




# parse_indeed()
