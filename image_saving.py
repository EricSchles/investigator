import requests
from .models import BackpageAdInfo as B

def image_url_parse(image_urls):
    return image_urls.lstrip("{").rstrip("}").split(",")

def save_locally(image_url,current_count):
    page = requests.get(image_url)
    if page.status_code == 200:
        with open(str(current_count)+".jpg",'wb') as f:
            f.write(page.content)
    with open("urls.txt","a") as f:
        f.write(image_url+"\n")

def main():
    import os
    os.chdir("app/static/images")
    with open("urls.txt","r") as f:
        urls_hit = f.read().split("\n")
    current_count = len(urls_hit)
    for elem in B.query.all():
        if elem.photos != '':
            image_urls = image_url_parse(elem.photos)    
            image_urls = [image_url for image_url in image_urls if image_url not in urls_hit]
            for image_url in image_urls:
                save_locally(image_url,current_count)
                current_count += 1

if __name__ =='__main__':
    main()
