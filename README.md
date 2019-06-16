# Tripadvisor_crawler
This project can help you scrape hotel information from Tripadvisor. I divide the process into two steps as following:
## Step1
 In **url_parser.py**, scrape all property types of hotels and save **url_parser.csv** in data folder  
 (including hotels' basic information ex. hotal name, url, number of comments, hotel rank in country, etc.) 
## Step2
 In **content_parser.py**, scrape hotels' detailed information baesd on Step1 output ex. hotel rank, phone number, numbers of comments in each rank, etc.
<!-- ## Step3
 In **data_manipulation.py**, do feature engineering or regular expression to extact content on Step2 output. -->

## Preparation 
1. Python2
2. Use Chromedriver or PhantomJS
3. Set your target_url, check in/out date in url_parser.py  
**Note: you can only choose current and next month for check in/out date** 
5. Turn off debug mode in content_parser.py

## Change
1. 2019/06: Added start/end date selector, property type selector, scraped main source and price.

## To Be Continued
If you have any feature requests, don't hesitate to contact me :)
1. Country selection
2. Room selection
3. Cookie usage

## Reference
1. Chromedriver: http://chromedriver.chromium.org  
**Note: Please notice the version compatibility between chrome and chromedriver**
