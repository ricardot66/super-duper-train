from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
import csv

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

with open('rappi.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    driver.get('https://www.rappi.com.mx/restaurantes')
    sleep(5)

    driver.find_element_by_xpath('/html/body/app-container/app-required-access/div/app-address-anonymous/app-modal/div/div/div[1]/div[2]/div[2]/div/div/div[1]/div/i').click()
    print('loading...')
    sleep(5)

    for i in range(100):
        try:
            sleep(3)
            driver.find_element_by_xpath('/html/body/app-container/div/div/span/app-by-stores-home/div/div[2]/div[2]/button').click()
            print('scrolling...')
        except:
            break

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    for i in soup.find_all('div', class_='store-item-box'):
        try:
            store_name = i.find('span', class_='store-name').text
        except:
            store_name = 'N/A'
        try:
            tags = i.find('span', class_='store-tags ng-star-inserted').text
        except:
            tags = 'N/A'

        try:
            for j in i.find_all('a', class_='store-item ng-star-inserted'):
                store_url = j['href']
        except:
            store_url = 'N/A'

        csv_writer.writerow([store_name, tags, store_url])


        print(store_name)
        print(tags)