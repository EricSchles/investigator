"""
Here we define our scrapers,  currently only backpage is defined.  The main work horse of this model is the scrape_backpage method.
Here we make use of text_parser.py as well as models.py.

test_coverage:

0% - this will be remedied soon.
"""
import requests
import lxml.html
import time
from app import db
from app.models import Backpage,BackpageAdInfo
from datetime import datetime
import random
from app.text_parser import phone_number_parse, get_lat_long,clean_location_string,strip_post_id
from app.nlp_tools import *

def check_for_repeat_ads(url, titles,ads,city,state):
    """
    This method checks for repeat ads.  The problem is ads update in a unpredictable fashion, therefore you don't want to store ads
    that you've already scraped.  This method checks the ad's already scraped and compares titles.  If the titles are different,
    then the ads can be assumed to be unique.
    Why can we do this?  Backpage kindly ads a unqiue number to the end of every ad for tracking purposes, therefore we are guaranteed uniqueness of title,
    if only because of the number appended to each ad, which is guaranteed to be unique.
    
    parameters:
    @titles - the titles is a list of strings, specifically the ad titles from the most recent scrape
    @ads - the ads are the urls to individual ads, they are unicode objects or strings.

    Notes - we uniquely identify on title and then pass back the urls that don't currently exist in our system.
    """
    if BackpageAdInfo.query.all() != []:
        unique_titles = set([elem.ad_title for elem in BackpageAdInfo.query.all()])
    else:
        unique_titles = []
    new_ads = []
    new_unique_titles = []
    for ind,val in enumerate(titles):
        if val in unique_titles:
            continue
        else:
            new_ads.append(ads[ind])
            new_unique_titles.append(val)
    for ind,unique_title in enumerate(new_unique_titles):
        phone_number, ad_body,location,latitude, longitude, post_id,timestamp,photo_urls = scrape_ad(new_ads[ind],city)
        if isinstance(timestamp,str):
            continue
        else:
            ad_info = BackpageAdInfo(new_ads[ind],unique_title,phone_number,ad_body,location,latitude,longitude,photo_urls,post_id,timestamp,city,state)
            db.session.add(ad_info)
            db.session.commit()
    return new_ads    

def clean_string(string):
    return string.strip().encode("ascii","ignore")

def scrape_backpage(url, city, state):
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
        try:
            html = lxml.html.fromstring(clean_string(r.text))
        except lxml.etree.ParserError:
            html = lxml.html.fromstring(r.text.encode('utf-8','strict'))
        ads = html.xpath("//div[contains(@class, 'cat')]/a/@href")
        #handles ads we've already scraped once to avoid over counting
        titles = [elem.text_content() for elem in html.xpath("//div[contains(@class, 'cat')]/a")]
        ads = check_for_repeat_ads(url, titles, ads, city, state)
        if len(ads) == 0:
            continue
        bp = Backpage(datetime.now(),len(ads))
        db.session.add(bp)
        db.session.commit()
        time.sleep(random.randint(2, 7))

def scrape_ad(url,city):
    r = requests.get(url)
    html = lxml.html.fromstring(clean_string(r.text))
    try:
        ad_body = [elem.text_content().replace("\r","") for elem in html.xpath("//div[@class='postingBody']")][0]
    except IndexError:
        #this means we don't have an ad body and thus there will be little to no useful information here.
        #and therefore we return only empty strings
        return '','','','','','',''
    extra_info = html.xpath("//div[@style='padding-left:2em;']")
    try:
        location = [elem.text_content() for elem in extra_info if "Location:" in elem.text_content()][0]
        location = clean_location_string(location)
        latitude,longitude = get_lat_long(location,city)
    except:
        latitude,longitude = '',''
    try:
        post_id = [elem.text_content() for elem in extra_info if "Post ID:" in elem.text_content()][0]
        post_id = strip_post_id(post_id)
    except IndexError:
        post_id = ''
    try:
        photo_urls = html.xpath("//ul[@id='viewAdPhotoLayout']//img/@src")
    except:
        photo_urls = ''
    other_ads = [elem for elem in html.xpath("//a/@href") if "backpage" in elem]
    phone_number = phone_number_parse(ad_body)
    return phone_number, ad_body,location,str(latitude),str(longitude),post_id,datetime.now(), photo_urls
