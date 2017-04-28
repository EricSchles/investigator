from app import scrapers

url_places = [("http://newyork.backpage.com/WomenSeekMen/","NYC")]

for url_place in url_places:
    print("starting scraper..")
    scrapers.scrape_backpage(url_place[0],url_place[1])
    print("running scraper")
