"""

Here the models for our database is defined.

I am using Postgres, Flask-SQLAlchemy for this application.

For an introduction to Flask-SQLAlchemy check out: http://flask-sqlalchemy.pocoo.org/2.1/
""" 
from app import db

class BackpageAdInfo(db.Model):
    """
    This model gives us a set of specific information from each add scraped from backpage.
    
    parameters:
    @ad_title - used primarily to uniquely identify backpage ads - since titles are unique
    @phone_number - the phone number used in the ad, can be empty.  This number is stored as a string
    since it should be thought of as immutable.
    @location - the location mentioned in the advertisement 
    @latitude - latitude derived from the location mentioned in the advertisement
    @longitude - longitude derived from the location mentioned in the advertisement
    @ad_body - the long form text in the ad
    @photos - a filepath link to the set of pictures downloaded for the ad
    @post_id - an id for each backpage post from backpage
    @timestamp - when the ad was scraped
    """
    __tablename__ = 'ad_info'
    id = db.Column(db.Integer, primary_key=True)
    ad_title = db.Column(db.String)
    phone_number = db.Column(db.String)
    location = db.Column(db.String)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    ad_body = db.Column(db.String)
    photos = db.Column(db.String)
    post_id = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    
    def __init__(self,ad_title,phone_number,ad_body,location,latitude,longitude,photos,post_id,timestamp):
        self.ad_title = ad_title
        self.phone_number = phone_number
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.ad_body = ad_body
        self.photos = photos
        self.post_id = post_id
        self.timestamp = timestamp
        
        
class Backpage(db.Model):
    """
    This model gives us high level information about backpage, the website.
    It is used to determine some metrics found in lectures/scraping_the_web.md
    
    parameters:
    @timestamp - this is the time at which the content was scraped, it is assumed scrapers will run all the time,
    therefore the scrape time should be accurate to within an hour of scraping, this is used in some of the metrics
    for analysis.
    @frequency - this is the number of ads scraped at @timestamp and is used in many of the metrics for the scraper.
    """
    __tablename__ = 'backpage'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    frequency = db.Column(db.Integer)
    
    def __init__(self,timestamp,frequency):
        self.timestamp = timestamp
        self.frequency = frequency
        
