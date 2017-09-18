import requests
from app.models import BackpageAdInfo as B
from app.models import ImageToText
from app import db
from elasticsearch import Elasticsearch
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np
import os
from glob import glob

host = "http://localhost:9200"
es = Elasticsearch(host)

def save_locally(image_url, current_count, meta_data):
    if image_url.startswith("http"):
        page = requests.get(image_url)
        if page.status_code == 200:
            filename = str(current_count)+".jpg"
            with open(filename,'wb') as f:
                f.write(page.content)
            image_metadata = ImageToText(
                image_url,
                filename,
                '',
                meta_data.state,
                meta_data.city,
                meta_data.location,
                meta_data.url,
                meta_data.timestamp,
                meta_data.phone_number,
                meta_data.latitude,
                meta_data.longitude)
            db.session.add(image_metadata)
            db.session.commit()


def db_list_parse(db_list):
    return db_list.lstrip("{").rstrip("}").split(",")


def image_to_objects(img_path):
    model = VGG16(weights='imagenet')
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)    
    return [label[1] for label in decode_predictions(preds, top=3)[0]]


index_name = "image_search_index"
image_to_labels = {}
os.chdir("app/static/images")
urls_hit = [elem.image_url for elem in ImageToText.query.all()]

print("started downloading locally")
current_count = len(urls_hit)
for elem in B.query.all():
    if elem.photos != '':
        image_urls = db_list_parse(elem.photos)    
        image_urls = [image_url for image_url in image_urls if image_url not in urls_hit]
        for image_url in image_urls:
            save_locally(image_url, current_count, elem)
            current_count += 1
print("finished downloading locally")

print("started processing images")
urls_hit = [elem.image_url for elem in ImageToText.query.all()]
for image_url in urls_hit:
    meta_data = ImageToText.query.filter_by(image_url=image_url).first()
    if meta_data.filename not in list(image_to_labels.keys()):
        labels = image_to_objects(meta_data.filename)
        data = {}
        for label in labels:
            data["label"] = label
            data["file"] = meta_data.filename
            data["phone_number"] = meta_data.phone_number
            data["state"] = meta_data.state
            data["city"] = meta_data.city
            data["location"] = meta_data.location
            data["url"] = meta_data.url
            data["timestamp"] = meta_data.timestamp
            data["image_url"] = image_url
            es.index(index=index_name, doc_type="txt", body=data)
print("finished processing images")
