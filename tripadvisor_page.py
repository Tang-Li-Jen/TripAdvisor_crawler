import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
#import re
import time

path ='/Users/charlie/Desktop/Tripadvisor/'

#driver = webdriver.Chrome(path + 'chromedriver')
driver = webdriver.PhantomJS()
driver.get('https://www.tripadvisor.com.tw/Hotels-g294225-Indonesia-Hotels.html')
driver.set_window_size(2560, 1600)
print driver.get_window_size()
#driver.maximize_window()
#print driver.get_window_size()
soup = BeautifulSoup(driver.page_source, 'html.parser')
domain = 'https://www.tripadvisor.com.tw'

# columns
hotel_name = []
url = []
address =[]
phone = []
n_comment = []
rank = []
comment_star = []
p_Excellent = []
p_VeryGood = []
p_Average = []
p_Poor = []
p_Terrible = []
price_range = []
hotel_star = []
hotel_url = []
gmap_src = []


# scrape page
next_page = '//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/span[2]'
check_last_page = '#taplc_main_pagination_bar_dusty_hotels_resp_0 > div > div > div > div > span.pageNum.last.taLnk'
page_down = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"

for p in range(int(soup.select(check_last_page)[0].get('data-page-number'))):
    print 'the number of page = {}'.format(p)
    for element in soup.find_all('div', {"class": "listing_title"}):
        hotel_name.append(element.text)
        url.append(domain+element.find('a').get('href'))
    driver.execute_script(page_down)
    time.sleep(5)
    driver.find_element_by_xpath(next_page).click()

df = pd.DataFrame({'hotel_name':hotel_name, 'url':url })

df.to_csv(path+'TripAdvisor_page.csv', index=False, encoding='utf-8')

# scrape content
df = pd.read_csv(path+'TripAdvisor_page.csv')
for u in df.url:
    print u
    driver.get(u)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # info_block
    info_block = soup.find('div', {'id':"atf_header"})
    address.append(info_block.find('span', {'class':"detail"}).text)
    try:
        phone.append(info_block.find('span', {'class':"is-hidden-mobile detail"}).text)
    except AttributeError:
        phone.append(None)
    n_comment.append(info_block.find('span', {'class':"reviewCount"}).text)
    rank.append(info_block.find('span', {'class':"header_popularity popIndexValidation"}).text)
    comment_star.append(soup.find('span', {'class':'overallRating'}).text)
    # about_block
    about_block = soup.find('div', {'class':"ui_column is-12-mobile is-6-tablet"})
    price_range.append(about_block.find('div', {'class':'textitem'}).text)
    # star
    try:
        hotel_star.append(soup.find('div', {'class':'starRating detailListItem'}).text)
    except AttributeError:
        hotel_star.append(None)
    # rating_chart
    rating_chart = soup.find('ul', {'class':"ratings_chart"})
    p_Excellent.append(rating_chart.find_all('span', {'class':'row_count row_cell'})[0].text)
    p_VeryGood.append(rating_chart.find_all('span', {'class':'row_count row_cell'})[1].text)
    p_Average.append(rating_chart.find_all('span', {'class':'row_count row_cell'})[2].text)
    p_Poor.append(rating_chart.find_all('span', {'class':'row_count row_cell'})[3].text)
    p_Terrible.append(rating_chart.find_all('span', {'class':'row_count row_cell'})[4].text)
    gmap_src.append(soup.find('img').get("src"))
    try:
        driver.find_element_by_css_selector('#taplc_resp_hr_atf_hotel_info_0 > div > div.ui_column.is-12-tablet.is-2-mobile.hotelActionsColumn > div > div > div > div.is-hidden-mobile.blEntry.website.ui_link > span.blue_test.detail').click()
        driver.switch_to_window(driver.window_handles[1])
        hotel_url.append(driver.current_url)
        #print driver.current_url
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
    except:
        hotel_url.append(None)



df = pd.DataFrame({
'hotel_name':hotel_name, 'url':url, 
    'address':address, 'n_comment':n_comment,'rank':rank, 'phone':phone, 'comment_star':comment_star,
                 'p_Excellent':p_Excellent, 'p_VeryGood':p_VeryGood, 'p_Average':p_Average,
                  'p_Poor':p_Poor, 'p_Terrible':p_Terrible,
                  'price_range':price_range, 'hotel_star':hotel_star, 'hotel_url':hotel_url, 'gmap_src':gmap_src
                })

df.to_csv(path+'TripAdvisor_all.csv', index=False, encoding='utf-8')

driver.close()