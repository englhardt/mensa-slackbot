import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from openmensa import OpenMensa

MRI_URL = "https://www.casinocatering.de/speiseplan/max-rubner-institut"
KIT_URL = "https://www.sw-ka.de/en/essen/"

def parse_mri_food(url=MRI_URL, prune_side_dishes=True):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    food = []
    for f in soup.find_all(attrs='views-field-field-fc-gericht-name'):
        f = re.sub('<su[pb]>.*?</su[bp]>', ' ', str(f))
        f = re.sub('<[^<]+>', '', f)
        food.append(f.strip())
    return food if not prune_side_dishes else food[:2]

def parse_kit_food(id=31, threshold=1.5,
                   minify_categories=['Cafeteria', '[pizza]werkPizza', '[pizza]werkPasta', '[pizza]werkSalate', '[kœri]werk', 'Schnitzelbar']):
    food = []
    raw_food = OpenMensa.get_meals_by_day(id, datetime.today().strftime('%Y-%m-%d'))
    for f in raw_food:
        if f['prices']['students'] is not None and f['prices']['students'] > threshold \
            and not any(a in f['category'] for a in minify_categories):
            food.append(f"{f['category']}: {f['name']}")
    cat_open = [c for c in minify_categories if any(c in f['category'] for f in raw_food)]
    food.append(f"_Other open lines:_ {', '.join(cat_open)}")
    return food

def build_food_message():
    food_mri = '\n'.join(parse_mri_food(MRI_URL))
    food_kit = '\n'.join(parse_kit_food())

    food = f"\nFood for <!date^{int(datetime.now().timestamp())}" + "^{date_long}|today>\n"
    food += f"*MRI* <{MRI_URL}|(Link)>\n{food_mri if len(food_mri) > 0 else '_closed today_'}\n"
    food += f"*KIT* <{KIT_URL}|(Link)>\n{food_kit if len(food_kit) > 0 else '_closed today_'}\n"
    return food
