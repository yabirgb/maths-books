import bottlenose
from bs4 import BeautifulSoup
import json

import csv
import re

from collections import Counter

import time

import random
from urllib.error import HTTPError

def error_handler(err):
    ex = err['exception']
    print("error")
    if isinstance(ex, HTTPError) and ex.code == 503:
        time.sleep(random.expovariate(0.1))
        return True

AWS_ACCESS_KEY_ID = "YOURACCESSKEY"
AWS_SECRET_ACCESS_KEY = "YOURSECRETKEY"
AWS_ASSOCIATE_TAG = "YOURID"
amazon = bottlenose.Amazon(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG, Region = "ES", ErrorHandler=error_handler, Parser=lambda text: BeautifulSoup(text, 'xml'))


a = []

with open('libros.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        search = re.search("(?P<url>https?://rads.[^\s]+)", row[8])
        if search:
            a.append(search.group("url")[41:51])

new_list = [a[i:i+6] for i in range(0, len(a), 6)]

dic = {}

k = 0

for n in new_list:
    response = amazon.ItemLookup(ItemId=",".join(n), ResponseGroup="Large",
    			SearchIndex="Books", IdType="ISBN")

    for item in response.ItemLookupResponse.Items:
        try:
            title = item.ItemAttributes.Title.text
        except:
            title = None

        try:
            author = item.ItemAttributes.Author.text
        except:
            author = None

        try:
            published = item.ItemAttributes.PublicationDate.text
        except:
            published = None

        try:
            publisher = item.ItemAttributes.Publisher.text
        except:
            publisher = None

        try:
            asin = item.ASIN.text
        except:
            asin = None

        try:
            isbn = item.ItemAttributes.ISBN.text
        except:
            isbn = None

        try:
            ean = item.ItemAttributes.EAN.text
        except:
            ean = None

        try:
            url = item.DetailPageURL.text
        except:
            url = None

        dic[asin] = {
            "title": title,
            "author": author,
            "published": published,
            "publisher": publisher,
            "asin": asin,
            "isbn": isbn,
            "ean": ean,
            "url": url,
            "image": None
        }

    images = amazon.ItemLookup(ItemId=",".join(n), ResponseGroup="Images",
    			SearchIndex="Books", IdType="ISBN")

    for item in images.ItemLookupResponse.Items:
        try:
            dic[item.ASIN.text]["image"] = item.LargeImage.URL.text
        except:
            image = None




    print("Done package" + str(k))

    with open("data_" + str(k) + ".json", "w+") as f:
        f.write(json.dumps(dic))

    print("Saved package" + str(k))
    dic = {}
    k+= 1
