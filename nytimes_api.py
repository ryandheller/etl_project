import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from requests_html import HTMLSession, user_agent
from tqdm import tqdm
import subprocess
import time
from datetime import datetime, timedelta
import json
import glob

#access token for api
api_key = "REVeQu6ErJR69xuO8n21kyuUA0Xt4lV1"
# first published date online
starts_date = "02/13/11"
#convert to Y-M-D
start_date = datetime.strptime(starts_date, "%m/%d/%y")
# create a list of list publication dates
date_list=[]
while start_date <= datetime.today():
    date_list.append(start_date.strftime('%Y-%m-%d'))
    start_date = (start_date + timedelta(days=7))
# take dates to create a list of api urls for all dates
def make_url(date):
    url = f"https://api.nytimes.com/svc/books/v3/lists/{date}/combined-print-and-e-book-fiction.json?api-key={api_key}"
    return url
api_urls = []
for date in date_list:
    api_url = make_url(date)
    api_urls.append(api_url)

# download the api files
def download_api_files(url):
    data = requests.get(url).json()
    fullname = "api_download\ "+ url.split('/')[7] + ".json"
    with open(fullname, 'w') as outfile:  
        json.dump(data, outfile)

#only download new api files
api_list = [x for x in glob.glob('api_download/*.json')]
downloaded_dates = []
for api in api_list:
    date = (api.split('\ ')[1].split('.')[0])
    downloaded_dates.append(date)

for url in api_urls:
    url_date = url.split('/')[7]
    if url_date in downloaded_dates:
        'alreaady downloaded'
    else:
        print(url_date)
        download_api_files(url)

    