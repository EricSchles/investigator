import asyncio
import requests
from app.models import BackpageAdInfo as B

def image_url_parse(image_urls):
    return image_urls.lstrip("{").rstrip("}").split(",")

def save_locally(image_url,current_count):
    page = requests.get(image_url)
    if page.status_code == 200:
        with open(str(current_count)+".jpg",'wb') as f:
            f.write(page.content)
    with open("urls.txt","a") as f:
        f.write(image_url+"\n")

if __name__ == '__main__':
    current_count = len(urls_hit)
    with open("urls.txt","r") as f:
        urls_hit = f.read().split("\n")

    for elem in B.query.all():
        if elem.photo_url != '':
            image_urls = image_url_parse(elem.photo_url)    
            image_urls = [image_url for image_url in image_urls if image_url not in urls_hit]
            for image_url in image_urls:
                save_locally(image_url,current_count)
                current_count += 1
