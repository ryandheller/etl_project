import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from requests_html import HTMLSession, user_agent
from tqdm import tqdm
import subprocess
import time
from datetime import datetime, timedelta
import csv
import json
import glob
import numpy as np
import pickle

count = 0
#grabbing the downloaded api files
api_list = [x for x in glob.glob('api_download/*.json')]
#creating list of dictionaries to be pickled later
dicts_list =[]
# gathering information for each book on the best sellers list, sending to dicts_list
for api in api_list:
    with open(api) as f:
        data = json.load(f)
        dicts = []
        date = data.get('results').get('published_date')
        books = data.get('results').get('books')[:15]
        for book in books:
            rank = book.get('rank')
            title = book.get('title')
            author = book.get('author')
            amazon_url = book.get('amazon_product_url')
            book_dict={"rank":rank,"title":title, "author":author,"amazon_url":amazon_url,"date":date}
            dicts.append(book_dict)
    # count is just to check where the file is at while running
    count += 1
    print(count)
    dicts_list.append(dicts)

#pickle dicts_list for later use
with open('ny_times_dict.pkl', 'wb') as g:
    pickle.dump(dicts_list, g, pickle.HIGHEST_PROTOCOL)

#check pickling
with open('ny_times_dict.pkl','rb') as handle:
    b = pickle.load(handle)
print(len(dicts_list))
print(dicts_list == b)