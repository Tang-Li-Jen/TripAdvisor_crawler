# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
import requests
import time
import csv
import re

options = webdriver.ChromeOptions()
# options.add_argument('headless')
target_url = 'https://www.tripadvisor.com.tw/Hotels-g294225-Indonesia-Hotels.html'
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.get(target_url)
# driver.maximize_window()

# Property Type expand all
expand_all = driver.find_element_by_xpath("""//*[@id="component_7"]/div/div[2]/div[3]/div[2]/div[7]/span""")
expand_all.click()

for i in range(2, 13):
    checkbox = driver.find_element_by_xpath('//*[@id="component_7"]/div/div[2]/div[3]/div[2]/div[%i]/div/label/div/span[1]/a/span' %i)
    checkbox.click()

soup = BeautifulSoup(driver.page_source, 'html.parser')
domain = 'https://www.tripadvisor.com.tw'

# scrape page
next_page = '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/span[2]'
check_last_page = '#taplc_main_pagination_bar_dusty_hotels_resp_0 > div > div > div > div > span.pageNum.last.taLnk'
page_down = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
page_list = range(int(soup.select(check_last_page)[0].get('data-page-number')))
print("Total number of page: {}".format(len(page_list)))

with open('./data/url_parser.csv', 'a') as csvfile:
    fieldnames = ['hotel_id', 'hotel_name', 'n_comment', 'rank_in_country', 'url']
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
            writer.writerow(
                            {
                                'hotel_id':index,
                                'hotel_name':hotel_name.encode("utf-8"),
                                'n_comment':n_comment,
                                'rank_in_country':rank_in_country.encode("utf-8"),
                                'url':url
                            }
                           )
        try:
            driver.execute_script(page_down)
            time.sleep(10)
            driver.find_element_by_xpath(next_page).click()
            time.sleep(10)
        except:
            print('in the end')

driver.quit()