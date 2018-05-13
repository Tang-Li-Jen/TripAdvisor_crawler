import pandas as pd
import numpy as np
import re

path = '/Users/charlie/Desktop/Tripadvisor/' 
df = pd.read_csv(path+'TripAdvisor_full.csv')

df['n_comment'] = df['n_comment'].apply(lambda x : re.sub('[^0-9,]', "", x).replace(',',''))
#df['rank'] = df['rank'].apply(lambda x : re.findall('\d+', x))
df['hotel_star'] = df['hotel_star'].apply(lambda x : re.sub('[^0-9,]', "", x))
df['lat'] = df['gmap_src'].apply(lambda x : re.findall(r"(.*)\,", re.findall(r"png\|(.*)\&signature", x)[0])[0])
df['lon'] = df['gmap_src'].apply(lambda x : re.findall(r"\,(.*)", re.findall(r"png\|(.*)\&signature", x)[0])[0])
df = df.drop(['gmap_src'],1)

df.to_csv(path+ 'TripAdvisor_FirstPage.csv', index=False, encoding='utf-8')