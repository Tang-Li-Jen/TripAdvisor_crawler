# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import requests
import time
import csv
import re

options = webdriver.ChromeOptions()
# options.add_argument('headless')
target_url = 'https://www.tripadvisor.com.tw/Hotels-g293808-Madagascar-Hotels.html'
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.get(target_url)
driver.maximize_window()

# Start date
select_start_date = driver.find_element_by_xpath("""//*[@id="PERSISTENT_TRIP_SEARCH_BAR"]/div[1]/div/div[2]/div[1]/div/span[2]/span[2]""")
select_start_date.click()

start_date = '27-June 2019'

start_date_splitter = start_date.split('-')
start_day, start_month_year = start_date_splitter[0], start_date_splitter[1]

for i in [1, 2]:
    year_month = driver.find_element_by_xpath("""//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/span/div[3]/div/div[2]/div[3]/span[{}]/span[1]""".format(i))
    if year_month.text == str(start_month_year):
        for j in range(3, 45):
            day_selector = driver.find_element_by_xpath("""//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/span/div[3]/div/div[2]/div[3]/span[{}]/span[{}]""".format(i,j))
            if day_selector.text == str(start_day):
                day_selector.click()
                break

time.sleep(30)

# Property Type 
## expand all
try:
    expand_all = driver.find_element_by_xpath("""//*[@id="component_6"]/div/div[2]/div[3]/div[2]/div[7]/span""")
    expand_all.click()
    component_id = 'component_6'
except:
    expand_all = driver.find_element_by_xpath("""//*[@id="component_7"]/div/div[2]/div[3]/div[2]/div[7]/span""")
    expand_all.click()
    component_id = 'component_7'

# select_checkbox_8 = driver.find_element_by_xpath('//*[@id="checkbox_8"]')
# driver.execute_script("arguments[0].click();", select_checkbox_8)

## select all property type
soup = BeautifulSoup(driver.page_source, 'html.parser')
tmp = soup.find_all('div', {"class": "common-filters-FilterWrapper__content--3RxLJ"})
num_of_property_type = len(tmp[2].find_all('div', {'class':'common-filters-CheckboxList__checkboxWrapper--3_ghM'}))

for i in range(2, num_of_property_type+1):
    checkbox = driver.find_element_by_xpath('//*[@id="{0}"]/div/div[2]/div[3]/div[2]/div[{1}]/div/label/div/span[1]/a/span'.format(component_id, i))
    checkbox.click()

time.sleep(20)

soup = BeautifulSoup(driver.page_source, 'html.parser')
domain = 'https://www.tripadvisor.com.tw'

# scrape page
next_page = '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/span[2]'
check_last_page = '#taplc_main_pagination_bar_dusty_hotels_resp_0 > div > div > div > div > span.pageNum.last.taLnk'
page_down = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
page_list = range(int(soup.select(check_last_page)[0].get('data-page-number')))
print("Total number of page: {}".format(len(page_list)))

with open('./data/url_parser.csv', 'a') as csvfile:
    fieldnames = ['hotel_id', 'hotel_name', 'main_source', 'main_price', 'n_comment', 'rank_in_country', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    index = 0

    for p in page_list[:2]:
        print('the number of page = {0}/{1}'.format(p+1, len(page_list)))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        hotel_blocks = soup.find_all('div', {"class": "prw_rup prw_meta_hsx_responsive_listing ui_section listItem"})

        for element in hotel_blocks:
            index += 1
            hotel_name = element.find('div', {"class": "listing_title"}).text
            url = domain+element.find('div', {"class": "listing_title"}).find('a').get('href')
            n_comment = element.find('a', {"class": "review_count"}).text
            n_comment = re.sub('[^0-9,]', "", n_comment).replace(',','')
            rank_in_country = element.find('div', {"class": "popindex"}).text

            price_and_source = element.find('div', {'class':'priceBlock ui_column is-12-tablet'})
            main_price = price_and_source.find('div', {'class':'price __resizeWatch'}).text
            main_source = price_and_source.find('span', {'class':'provider_text'}).text

            writer.writerow(
                            {
                                'hotel_id':index,
                                'hotel_name':hotel_name.encode("utf-8"),
                                'main_source':main_source.encode("utf-8"),
                                'main_price':main_price,
                                'n_comment':n_comment,
                                'rank_in_country':rank_in_country.encode("utf-8"),
                                'url':url
                            }
                           )
        try:
            driver.execute_script(page_down)
            time.sleep(15)
            driver.find_element_by_xpath(next_page).click()
            time.sleep(15)
        except:
            print('in the end')

driver.quit()