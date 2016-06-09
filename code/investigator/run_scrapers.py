from app import scrapers

urls = ["http://newyork.backpage.com/FemaleEscorts/"]

for url in urls:
    print("starting scraper..")
    scrapers.scrape_backpage()
    print("running scraper")
