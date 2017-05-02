import csv
import re

a = 0

with open('libros.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        search = re.search("(?P<url>https?://rads.[^\s]+)", row[8])
        if search:
            print(search.group("url")[41:51])
            a += 1

print(a)
