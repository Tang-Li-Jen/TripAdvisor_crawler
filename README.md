# Tripadvisor_crawler
This project can help you scrape hotel information from Tripadvisor. I divide the process into two steps as following:
## Step1
 In **url_parser.py**, scrape and save **url_parser.csv** on data folder  
 (including hotels' basic information ex. hotal name, url, number of comments, hotel rank in country, etc.) 
## Step2
 In **content_parser.py**, scrape hotels' detailed information baesd on Step1 output ex. hotel rank, phone number, numbers of comments in each rank, etc.
<!-- ## Step3
 In **data_manipulation.py**, do feature engineering or regular expression to extact content on Step2 output. -->

## Preparation 
1. Python2
2. Use Chromedriver or PhantomJS
3. Set your target_url in url_parser.py
4. Turn off debug mode in content_parser.py
 
## To Be Continued
If you have any feature requests, don't hesitate to contact me :)
1. Country selection
2. Date selection
3. Room selection
4. Cookie usage

## Reference
1. Chromedriver: http://chromedriver.chromium.org
