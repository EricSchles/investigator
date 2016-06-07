from app import db

class AdInfo(db.Model):
    __tablename__ = 'ad_info'
    id = db.Column(db.Integer, primary_key=True)
    ad_title = db.Column(db.String)

    def __init__(self,ad_title):
        self.ad_title = ad_title
        
class Backpage(db.Model):
    __tablename__ = 'backpage'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    frequency = db.Column(db.Integer)
    
    def __init__(self,timestamp,frequency):
        self.timestamp = timestamp
        self.frequency = frequency
        
