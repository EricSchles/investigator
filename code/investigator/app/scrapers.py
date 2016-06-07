import requests
import lxml.html
import time
from app import db
from app.models import Backpage,AdInfo
from datetime import datetime
import random

def check_for_repeat_ads(titles,ads):
    unique_titles = [elem.ad_title for elem in AdInfo.query.all()]
    new_ads = []
    new_unique_titles = []
    for ind,val in enumerate(titles):
        if val in unique_titles:
            continue
        else:
            new_ads.append(ads[ind])
            new_unique_titles.append(val)
    for unique_title in new_unique_titles:
        ad_info = AdInfo(unique_title)
        db.session.add(ad_info)
        db.session.commit()
    return new_ads

def scrape_backpage():
    while True:
        r = requests.get("http://newyork.backpage.com/FemaleEscorts/")
        html = lxml.html.fromstring(r.text)
        ads = html.xpath("//div[contains(@class, 'cat')]/a/@href")
        #handles ads we've already scraped once to avoid over counting
        titles = [elem.text_content() for elem in html.xpath("//div[contains(@class, 'cat')]/a")]
        ads = check_for_repeat_ads(titles,ads)
        if len(ads) == 0:
            continue
        bp = Backpage(datetime.now(),len(ads))
        db.session.add(bp)
        db.session.commit()
        time.sleep(random.randint(2,700))
