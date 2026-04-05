import json
from  borsaitaliana import borsa_italiana

class Scraper:

    def __init__(self):
        pass

    def scrape(self, *arg):
        pass




def load_file(f):
    pass


isin='XS2419364653'
market='MOT'

p = f"www/eod/xmil/{isin}.json"
f = open(p, "r")
j = json.load(f)
f.close()
d1 = {}
for date, price in j:
    d1[date] = price

print(len(d1))
ultimo = j[-1][0]
l = borsa_italiana(isin, market)
for date, price in l:
    d1[date] = price

print(len(d1))