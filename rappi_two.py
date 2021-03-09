from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json
from time import sleep
import csv

with open('rappi_urls.csv', 'r') as csv_file:
    with open('restaurant_info.csv', 'a') as csv_output:
        csv_writer = csv.writer(csv_output)
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        sleep(6)

        csv_writer.writerow(["name", "url", "address", "latitude", "longitude", "product_name", "price"])

        for restaurant in csv_file:
            driver.get('https://www.rappi.com.mx' + str(restaurant))
            sleep(3)
            try:
                driver.find_element_by_xpath(
                    '/html/body/app-container/app-required-access/div/app-address-anonymous/app-modal/div/div/div[1]/div[2]/div[2]/div/div/div[1]/div/i').click()
            except:
                print('no more')
            print('loading...')

            sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html)

            for i in soup.find_all('div', class_='product-detail'):
                product_name = i.find('h3', class_='product-name').text
                price = i.find('span', class_='product-price f-caption-1').text

                new_soup = str(soup.find_all('article')[3])
                pre_soup = new_soup.replace('<article _ngcontent-ng-web-c35=""><script type="application/ld+json">', '')
                new_json = pre_soup.replace('</script></article>', '')

                try:
                    r = json.loads(new_json)
                    address = r['address']['streetAddress']
                    latitude = r['geo']['latitude']
                    longitude = r['geo']['longitude']
                    name = r['name']
                except:
                    address = 'N/A'
                    latitude = 'N/A'
                    longitude = 'N/A'
                    name = 'N/A'

                csv_writer.writerow([name, restaurant, address, latitude, longitude, product_name, price])

                print(str(name) + ' done!')

    driver.quit()
