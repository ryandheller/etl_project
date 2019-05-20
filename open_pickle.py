import pickle
import csv
import pymongo
from pymongo import MongoClient

#open both pkl files
with open('ny_times_dict.pkl','rb') as handle:
    ny_times = pickle.load(handle)

with open('amazon_prices.pkl','rb') as handle:
    amazon = pickle.load(handle)
#zip together dictionaries for all books that had valid amazon urls
good_dicts = []
for listed in ny_times:
    for dicts in listed:
        try:
            title = dicts.get('amazon_url').split('/')[3]
        except:
            'oh whale'
        for item in amazon:
            if item.get('Title') == title:
                z = {**item, **dicts}
                good_dicts.append(z)
                
            else:
                ''
#create a list of amazon urls added to good_dicts
amazon_urls = []
for dicts in good_dicts:
    amazon_urls.append(dicts.get('amazon_url'))
#check and add any remaining books to good_dicts
for listed in ny_times:
    for dicts in listed:
        if dicts.get('amazon_url') in amazon_urls:
            'good to go'
        else:
            good_dicts.append(dicts)
#for those books that didn't return amazon prices append a blank
kindle = []
for dicts in good_dicts:
    if 'Kindle' in dicts.keys():
        kindle.append(dicts['Kindle'])
    else:
        dicts['Kindle']=float(0)
        kindle.append(dicts['Kindle'])
    if 'Hardcover' in dicts.keys():
        kindle.append(dicts['Hardcover'])
    else:
        dicts['Hardcover']=float(0)
        kindle.append(dicts['Kindle'])
    if 'Paperback' in dicts.keys():
        kindle.append(dicts['Paperback'])
    else:
        dicts['Paperback']=float(0)
        kindle.append(dicts['Kindle'])
    if 'Audio' in dicts.keys():
        kindle.append(dicts['Kindle'])
    else:
        dicts['Audio']= float(0)
        kindle.append(dicts['Kindle'])


# send dictionary to MongoDB
client = MongoClient()
db = client.NYT_best_sellers
db.info.remove()
db.info.insert(good_dicts)

