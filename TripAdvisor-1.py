import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
#import re
import time

path ='/Users/charlie/Desktop/Tripadvisor/'

#chromeOptions = webdriver.ChromeOptions()
#prefs = {'profile.managed_default_content_settings.images':2}
#chromeOptions.add_experimental_option("prefs", prefs)
#chrome_options=chromeOptions

#driver = webdriver.Chrome(path+'chromedriver.exe')
#driver.get('https://www.tripadvisor.com.tw/Hotels-g294225-Indonesia-Hotels.html')
#driver.set_window_size(1280, 1024)
#driver.page_source

r = requests.get('https://www.tripadvisor.com.tw/Hotels-g294225-Indonesia-Hotels.html') 
print(r.encoding)
#soup = BeautifulSoup(driver.page_source, 'html.parser')
soup = BeautifulSoup(r.text, 'html.parser')
domain = 'https://www.tripadvisor.com.tw'
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
i = 0
driver = webdriver.Chrome('/Users/charlie/Desktop/Crawler/chromedriver')
driver.set_window_size(1280, 1024)
#driver = webdriver.PhantomJS()
#driver.maximize_window()
for element in soup.find_all('div', {"class": "listing_title"}):
    print(i)
    hotel_name.append(element.text)
    url.append(domain+element.find('a').get('href'))
    #r2 = requests.get(domain+element.find('a').get('href'))
    driver.get(domain+element.find('a').get('href'))
    soup2 = BeautifulSoup(driver.page_source, 'html.parser')
    # info_block
    info_block = soup2.find('div', {'id':"atf_header"})
    address.append(info_block.find('span', {'class':"detail"}).text)
    try:
        phone.append(info_block.find('span', {'class':"is-hidden-mobile detail"}).text)
    except AttributeError:
        phone.append(None)
    n_comment.append(info_block.find('span', {'class':"reviewCount"}).text)
    rank.append(info_block.find('span', {'class':"header_popularity popIndexValidation"}).text)
    comment_star.append(soup2.find('span', {'class':'overallRating'}).text)
    # about_block
    about_block = soup2.find('div', {'class':"ui_column is-12-mobile is-6-tablet"})
    price_range.append(about_block.find('div', {'class':'textitem'}).text)
    # star
    try:
        hotel_star.append(soup2.find('div', {'class':'starRating detailListItem'}).text)
    except AttributeError:
        hotel_star.append(None)
    # rating_chart
    rating_chart = soup2.find('ul', {'class':"ratings_chart"})
    p_Excellent.append(rating_chart.find_all('span', {'class':'row_count row_cell'})[0].text)
    p_VeryGood.append(rating_chart.find_all('span', {'class':'row_count row_cell'})[1].text)
    p_Average.append(rating_chart.find_all('span', {'class':'row_count row_cell'})[2].text)
    p_Poor.append(rating_chart.find_all('span', {'class':'row_count row_cell'})[3].text)
    p_Terrible.append(rating_chart.find_all('span', {'class':'row_count row_cell'})[4].text)
    try:
        driver.find_element_by_css_selector('#taplc_resp_hr_atf_hotel_info_0 > div > div.ui_column.is-12-tablet.is-2-mobile.hotelActionsColumn > div > div > div > div.is-hidden-mobile.blEntry.website.ui_link > span.blue_test.detail').click()
        driver.switch_to_window(driver.window_handles[1])
        hotel_url.append(driver.current_url)
        print driver.current_url
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
    except:
        hotel_url.append(None)
    time.sleep(5)
    gmap_src.append(driver.find_element_by_css_selector('#taplc_hotel_detail_overview_responsive_0 > div > div.overviewContent > div > div.ui_column.is-shown-at-tablet.is-12.is-4-desktop > div > div > div > img').get_attribute("src"))
    #gmap_src.append(driver.find_element_by_xpath('//*[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[5]/div/div/div/img').get_attribute("src"))
    i += 1
driver.close()
df = pd.DataFrame({'hotel_name':hotel_name, 'url':url, 'address':address, 'n_comment':n_comment,'rank':rank, 'phone':phone, 'comment_star':comment_star,
                 'p_Excellent':p_Excellent, 'p_VeryGood':p_VeryGood, 'p_Average':p_Average,
                  'p_Poor':p_Poor, 'p_Terrible':p_Terrible,
                  'price_range':price_range, 'hotel_star':hotel_star, 'hotel_url':hotel_url, 'gmap_src':gmap_src
                })

df.to_csv(path+'TripAdvisor_full.csv', index=False, encoding='utf-8')



#    time.sleep(2)



