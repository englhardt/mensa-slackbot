import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from openmensa import OpenMensa

def parse_mri_food(url='https://www.casinocatering.de/speiseplan/max-rubner-institut'):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    food = []
    for f in soup.find_all(attrs='views-field-field-fc-gericht-name'):
        f = re.sub('<su[pb]>.*?</su[bp]>', '', str(f))
        f = re.sub('<[^<]+>', '', f)
        food.append(f.strip())
    return food

def parse_kit_food(id=31, treshold=2, avoid=['Cafeteria']):
    food = []
    for f in OpenMensa.get_meals_by_day(id, datetime.today().strftime('%Y-%m-%d')):
        if f['prices']['students'] is not None and f['prices']['students'] > treshold \
            and not any(a in f['category'] for a in avoid):
            food.append(f"{f['category']}: {f['name']} ({f['prices']['students']:.2f}/{f['prices']['employees']:.2f} €)")
    return food
