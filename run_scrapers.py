from app import scrapers

url_places = [("http://newyork.backpage.com/WomenSeekMen/","NYC","NY")]

for url_place in url_places:
    print("starting scraper..")
    scrapers.scrape_backpage(url_place[0], url_place[1], url_place[2])
    print("running scraper")
