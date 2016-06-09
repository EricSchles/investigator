#Getting hard attributes from a backpage ad

This step will be of the highest interest to investigators.  From their perspetive, this is just automating what they already do, and therefore will lead to a higher level of excitement than you might get otherwise.  Investigators are constantly overworked and under appreciated, so any automation that takes away a "boring" task will always be welcomed!

##Understanding the layout of ads on backpage

Backpage and craigslist both have a templated system for their ads - all ads follow the same structural layout, therefore once you've parsed one ad, you've parsed them all!

Here is a typical backpage female escort ad:

![](pictures/female_escort_ad.png)

###Getting the ad text body

A lot of semantic analysis can be done from the ad body (and don't worry, we will).  But first we'll pull out the text!

Rather than trying to fit this into our previous scheme of scraping, will just show the steps from a given backpage ad:

```
import requests
import lxml.html
r = requests.get("http://newyork.backpage.com/FemaleEscorts/incredible-edible-kandii-specials/79342904")
html = lxml.html.fromstring(r.text)
print([elem.text_content().replace("\r","") for elem in html.xpath("//div[@class='postingBody']")])
```

It's worth noting that this has a bunch of emoji's and ascii art which we might have to handle, via textacy's transliteration function. Rather than moving directly over to the database context, we'll define our metrics of interest and show how to pull those out first.

We'll be storing:

* phone numbers
* body of the ad
* location information
* ad pictures


