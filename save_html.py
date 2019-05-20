import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from requests_html import HTMLSession, user_agent
from tqdm import tqdm
import subprocess
from datetime import datetime, timedelta
import csv
import os
import glob
import pickle

# function to download amazon page html
def download_book_data_from_url(url):
    try:
        session = HTMLSession()
        r = session.get(url)
        r.html.render()
    except Exception as e:
        print('books borked!', e)
    soup = BeautifulSoup(r.html.html, "html.parser")
    fullname = "htmlFolder\ "+ url.split('/')[3] + ".html"
    print(fullname)
    with open(fullname, 'w', encoding="utf-8") as f:
        f.write(str(soup))
    

#gather the amazon urls from the best selling apis
with open('ny_times_dict.pkl','rb') as handle:
    b = pickle.load(handle)
amazon_urls = []
for a in b:
    for z in a:
        if z.get('amazon_url') != None:
            amazon_urls.append(z.get('amazon_url'))
        elif z.get('amazon_url') == None:
            ''
#by sending our list to a set we get rid of any repeats
amazon_set = set(amazon_urls)
print(len(amazon_urls), len(amazon_set))

counting = 0
# check to see if a book has already had it's html downloaded, if not download it
for url in amazon_set:
    new_u = url.split('/')[3]
    existing_files = [x.split('\\')[-1].strip() for x in glob.glob('htmlFolder/*.html')]
    existing_names = [x.split('.')[0].strip() for x in existing_files]
    if new_u == 'The-Lady-Rivers-Novel-Cousins?tag=NYTBS-20':
        print('get outta here', url)
    elif new_u not in existing_names:
            download_book_data_from_url(url)
            print('downloading', url)
    elif new_u in existing_names:
        'nothing'
        print('already downloaded')
    #counting is just to watch where the file is at when running
    counting += 1
    print(counting)
