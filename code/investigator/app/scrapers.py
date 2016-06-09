import requests
import lxml.html
import time
from app import db
from app.models import Backpage,BackpageAdInfo
from datetime import datetime
import random

def check_for_repeat_ads(titles,ads):
    """
    This method checks for repeat ads.  The problem is ads update in a unpredictable fashion, therefore you don't want to store ads
    that you've already scraped.  This method checks the ad's already scraped and compares titles.  If the titles are different,
    then the ads can be assumed to be unique.
    Why can we do this?  Backpage kindly ads a unqiue number to the end of every ad for tracking purposes, therefore we are guaranteed uniqueness of title,
    if only because of the number appended to each ad, which is guaranteed to be unique.
    
    parameters:
    @titles - the titles is a list of strings, specifically the ad titles from the most recent scrape
    @ads - the ads are the urls to individual ads

    Notes - we uniquely identify on title and then pass back the urls that don't currently exist in our system.
    """
    unique_titles = [elem.ad_title for elem in BackpageAdInfo.query.all()]
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
    
def scrape_backpage(url):
    """
    This method scrapes backpages female escort service. it is documented in some detail in lectures/technical_steps_for_second_backpage_crawler.md
    but just to clarify what's going on - we are simply going to the most recent ads on backpage and continuously scraping the ads new content.
    We only update our database when new information has been found.  It's worth noting that there is often a delay in the time when a poster, posts to backpage
    and when the ads show up.  So this will only capture market affects and market dynamics, not poster intention or poster behavior.  This is still enough to get
    a sense of market size and reaction.  But it's also worth noting that ads do get dropped from time to time.  
    
    parameters:
    @url - this is expected to be a string.  This is the url for the place we are scraping.  There is a lot of information encoded here - the location 
    we are scraping, defined by the subdomain and the part of backpage we are scraping, defined by everything after the '.com/'
    """
    
    while True:
        r = requests.get(url)
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

