import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
option = webdriver.ChromeOptions()
option.add_argument('headless')

driver = webdriver.Chrome('chromedriver', chrome_options=option)
driver.get('https://www.tripadvisor.com.tw/Hotels-g294225-Indonesia-Hotels.html')
driver.maximize_window()

soup = BeautifulSoup(driver.page_source, 'html.parser')
domain = 'https://www.tripadvisor.com.tw'

# columns
hotel_name = []
url = []
n_comment = []
rank_in_country = []

# scrape page
next_page = '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/span[2]'
check_last_page = '#taplc_main_pagination_bar_dusty_hotels_resp_0 > div > div > div > div > span.pageNum.last.taLnk'
page_down = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"

for p in range(int(soup.select(check_last_page)[0].get('data-page-number'))):
    print 'the number of page = {}'.format(p+1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for element in soup.find_all('div', {"class": "prw_rup prw_meta_hsx_responsive_listing ui_section listItem"}):
        hotel_name.append(element.find('div', {"class": "listing_title"}).text)
        url.append(domain+element.find('div', {"class": "listing_title"}).find('a').get('href'))
        n_comment.append(element.find('a', {"class": "review_count"}).text)
        rank_in_country.append(element.find('div', {"class": "popindex"}).text)
    try:
        driver.execute_script(page_down)
        time.sleep(5)
        driver.find_element_by_xpath(next_page).click()
        time.sleep(8)
    except:
        print('in the end')

df = pd.DataFrame({'hotel_name':hotel_name, 'url':url,
                   'n_comment':n_comment, 'rank_in_country':rank_in_country })

df.to_csv('url_parser.csv', index=False, encoding='utf-8')

driver.quit()