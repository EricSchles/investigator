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
from collections import namedtuple


AdInfo = namedtuple(
    'AdInfo',
    [
        'phone_number',
        'ad_body',
        'location',
        'latitude',
        'longitude',
        'post_id',
        'timestamp',
        'photos'
    ]
)


def check_for_repeat_ads(url, titles, ads, city, state):
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
    unique_titles = {elem.ad_title
                     for elem in BackpageAdInfo.query.all()}
    new_unique_titles, new_ads = [], []
    for title, ad in zip(titles,ads):
        if title not in unique_titles:
            new_ads.append(ad)
            new_unique_titles.append(title)
    return new_unique_titles, new_ads


def save_to_database(unique_titles, ads, city, state):
    for unique_title, ad in zip(unique_titles, ads):
        ad_info = scrape_ad(ad, city)
        if not isinstance(ad_info.timestamp, str):
            backpage_ad_info = BackpageAdInfo(
                ad,
                unique_title,
                city=city,
                state=state,
                **ad_info._asdict()
            )
            db.session.add(backpage_ad_info)
            db.session.commit()


def clean_string(string):
    return string.strip().encode("ascii","ignore")


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
        latitude, longitude = get_lat_long(location, city)
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
    ad_info = AdInfo(
        phone_number,
        ad_body,
        location,
        str(latitude),
        str(longitude),
        post_id,
        datetime.now(),
        photo_urls
    )
    return ad_info


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
    @city - the city being scraped (for USA)
    @state - the state being scraped (for USA)
    """
    
    while True:
        r = requests.get(url)
        try:
            cleaned_text = clean_string(r.text)
            html = lxml.html.fromstring(cleaned_text)
        except lxml.etree.ParserError:
            utf8_encoded_string = r.text.encode('utf-8','strict')
            html = lxml.html.fromstring(utf8_encoded_string)
        ads, titles = [], []
        for elem in html.xpath("//div[contains(@class, 'cat')]/a"):
            ad_url = elem.xpath("@href")[0]
            ads.append(ad_url)
            titles.append(elem.text_content())           
        unique_titles, unique_ads = check_for_repeat_ads(url, titles, ads, city, state)
        save_to_database(unique_titles, unique_ads, city, state)
        number_unique_ads = len(unique_ads)
        if number_unique_ads != 0:
            bp = Backpage(datetime.now(), number_unique_ads)
            db.session.add(bp)
            db.session.commit()

        time.sleep(random.randint(2, 7))

