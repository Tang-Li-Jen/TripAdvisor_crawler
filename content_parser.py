import pandas as pd
import csv
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

domain = 'https://www.tripadvisor.com.tw'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

df = pd.read_csv('./data/url_parser.csv')
total_hotels = len(df)
with open('./data/content_parser.csv', 'a') as csvfile:
    fieldnames = [
                    'hotel_id', 'address', 'rank', 
                    'phone','p_Excellent', 'p_VeryGood':, 'p_Average',
                    'p_Poor', 'p_Terrible'
                 ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i, u in df[['hotel_id','url']]:
        print('process = {}/{}'.format(i+1, total_hotels))
        r = requests.get(u, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        # info_block
        info_block = soup.find('div', {'id':"atf_header"})
        address = info_block.find('span', {'class':"detail"}).text
        try:
            phone = info_block.find('span', {'class':"is-hidden-mobile detail"}).text
        except AttributeError:
            phone = None
        rank = info_block.find('span', {'class':"header_popularity popIndexValidation"}).text
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
        p_Excellent = rating_chart.find_all('div', {'class':'ui_checkbox item'})[0].text
        p_VeryGood = rating_chart.find_all('div', {'class':'ui_checkbox item'})[1].text
        p_Average = rating_chart.find_all('div', {'class':'ui_checkbox item'})[2].text
        p_Poor = rating_chart.find_all('div', {'class':'ui_checkbox item'})[3].text
        p_Terrible = rating_chart.find_all('div', {'class':'ui_checkbox item'})[4].text
        # try:
        #     driver.find_element_by_css_selector('#taplc_resp_hr_atf_hotel_info_0 > div > div.ui_column.is-12-tablet.is-2-mobile.hotelActionsColumn > div > div > div > div.is-hidden-mobile.blEntry.website.ui_link > span.blue_test.detail').click()
        #     driver.switch_to_window(driver.window_handles[1])
        #     hotel_url = driver.current_url
        #     driver.close()
        #     driver.switch_to_window(driver.window_handles[0])
        # except:
        #     hotel_url = None
        writer.writerow(
                         {
                            'hotel_id':hotel_id,
                            'address':address,
                            'rank':rank,
                            'phone':phone,
                            'p_Excellent':p_Excellent, 
                            'p_VeryGood':p_VeryGood, 
                            'p_Average':p_Average,
                            'p_Poor':p_Poor, 
                            'p_Terrible':p_Terrible
                         }
                        )
        time.sleep(8)