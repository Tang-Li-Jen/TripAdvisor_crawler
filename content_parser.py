# -*- coding: utf-8 -*-
import pandas as pd
import csv
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import re

domain = 'https://www.tripadvisor.com.tw'
df = pd.read_csv('./data/url_parser.csv')
total_hotels = len(df)
debug = True
if debug:
    limit = 10
else:
    limit = None

with open('./data/content_parser.csv', 'a') as csvfile:
    fieldnames = [
                    'hotel_id', 'address', 'rank', 'phone',
                    'n_Excellent', 'n_VeryGood', 'n_Average', 'n_Poor', 'n_Terrible'
                 ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for index, u in enumerate(df['url'][:limit]):
        hotel_id = df['hotel_id'][index]
        print('process = {}/{}'.format(index+1, total_hotels))
        r = requests.get(u)
        soup = BeautifulSoup(r.text, 'html.parser')
        # info_block
        info_block = soup.find('div', {'id':"atf_header"})
        address = info_block.find('span', {'class':"detail"}).text
        try:
            phone = info_block.find('span', {'class':"is-hidden-mobile detail"}).text
        except AttributeError:
            phone = None
        rank = info_block.find('span', {'class':"header_popularity popIndexValidation"}).text

        # about_block
        about_block = soup.find('div', {'class':"hotels-hotel-review-layout-Section__plain--1HV0a"})

        # rating_chart
        rating_chart = soup.find('div', {'class':"choices"})
        rating_dict = {'Excellent':None,'VeryGood':None,'Average':None,'Poor':None,'Terrible':None}
        for i, col in enumerate(rating_dict):
            try:
                tmp = rating_chart.find_all('div', {'class':'ui_checkbox item'})[i].text
                tmp = int(re.sub('[^0-9,]', "", tmp).replace(',',''))
                rating_dict[col] = tmp
            except:
                rating_dict[col] = None
        writer.writerow(
                         {
                            'hotel_id':hotel_id,
                            'address':address,
                            'rank':rank.encode('utf-8'),
                            'phone':phone,
                            'n_Excellent':rating_dict["Excellent"], 
                            'n_VeryGood':rating_dict["VeryGood"], 
                            'n_Average':rating_dict["Average"],
                            'n_Poor':rating_dict["Poor"],
                            'n_Terrible':rating_dict["Terrible"]
                         }
                        )
        time.sleep(10)