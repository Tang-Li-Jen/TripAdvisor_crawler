import pandas as pd
import csv
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

domain = 'https://www.tripadvisor.com.tw'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

hotel_name = []
hotel_url = []
n_comment = []
address =[]
phone = []
rank = []
comment_star = []
p_Excellent = []
p_VeryGood = []
p_Average = []
p_Poor = []
p_Terrible = []
price_range = []
hotel_star = []

df = pd.read_csv('url_parser.csv')
total_len = len(df)
for index, u in enumerate(df.url[:10]):
    print 'process = {}/{}'.format(index+1, total_len)
    hotel_url.append(u)
    r = requests.get(u, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    hotel_name.append(soup.find('h1',{'class':'ui_header h1'}).text)
    # info_block
    info_block = soup.find('div', {'id':"atf_header"})
    address.append(info_block.find('span', {'class':"detail"}).text)
    try:
        phone.append(info_block.find('span', {'class':"is-hidden-mobile detail"}).text)
    except AttributeError:
        phone.append(None)
    n_comment.append(info_block.find('span', {'class':"reviewCount"}).text)
    rank.append(info_block.find('span', {'class':"header_popularity popIndexValidation"}).text)
    # comment_star.append(soup.find('span', {'class':'hotels-hotel-review-about-with-photos-Reviews__overallRating--3cjYf'}).text)

    # about_block
    about_block = soup.find('div', {'class':"hotels-hotel-review-layout-Section__plain--1HV0a"})
    # price_range.append(about_block.find('div', {'class':'hotels-hotel-review-about-addendum-AddendumItem__content--28NoV'}).text)

    # star
    # try:
    #     hotel_star.append(soup.find('div', {'class':'starRating detailListItem'}).text)
    # except AttributeError:
    #     hotel_star.append(None)

    # rating_chart
    rating_chart = soup.find('div', {'class':"choices"})
    p_Excellent.append(rating_chart.find_all('div', {'class':'ui_checkbox item'})[0].text)
    p_VeryGood.append(rating_chart.find_all('div', {'class':'ui_checkbox item'})[1].text)
    p_Average.append(rating_chart.find_all('div', {'class':'ui_checkbox item'})[2].text)
    p_Poor.append(rating_chart.find_all('div', {'class':'ui_checkbox item'})[3].text)
    p_Terrible.append(rating_chart.find_all('div', {'class':'ui_checkbox item'})[4].text)
    # gmap_src = soup.find('img').get("src")
    # try:
    #     driver.find_element_by_css_selector('#taplc_resp_hr_atf_hotel_info_0 > div > div.ui_column.is-12-tablet.is-2-mobile.hotelActionsColumn > div > div > div > div.is-hidden-mobile.blEntry.website.ui_link > span.blue_test.detail').click()
    #     driver.switch_to_window(driver.window_handles[1])
    #     hotel_url = driver.current_url
    #     driver.close()
    #     driver.switch_to_window(driver.window_handles[0])
    # except:
    #     hotel_url = None
    time.sleep(8)

df = pd.DataFrame({
    'hotel_name':hotel_name , 'hotel_url':hotel_url, 'address':address, 
    'n_comment':n_comment,'rank':rank, 'phone':phone,# 'comment_star':comment_star,
    'p_Excellent':p_Excellent, 'p_VeryGood':p_VeryGood, 'p_Average':p_Average,
    'p_Poor':p_Poor, 'p_Terrible':p_Terrible
    # 'price_range':price_range
    # 'hotel_star':hotel_star
                })

df.to_csv('content_parser.csv', index=False, encoding='utf-8')