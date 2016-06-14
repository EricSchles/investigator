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

###Parsing Address Information

Parsing addresses entails taking an address and translating it from text to latitude/longitude.  This is just one possible way to represent geographic information.  The general procedure is to go from something ambigious like text and to go to something specific and structured.  There are other possible representations for geographic coordinate systems that we won't discuss.  Parsing addresses can be a surprisingly hard thing to do - [this small treatise on stackover flow](http://stackoverflow.com/questions/11160192/how-to-parse-freeform-street-postal-address-out-of-text-and-into-components) details some of the diffculties.  For those of you without internet connection, I'll summarize the main points:

* Addresses are not regular
	* Addresses come in unexpected shapes and sizes

* You don't own address data or set the standard for address information
	
* We expect addresses to be hard, so they are complex.

Fortunately, we have a lot of tools for parsing addresses, specifically because it is such a hard problem.  

We'll start our survey of such tools with street-address.  To get it, open a terminal and type:

`pip install street-address`

This package is available for python 2 & 3.

Let's start by looking at a minimal example:

```
from streetaddress import StreetAddressParser

addr_parser = StreetAddressParser()
print(addr_parser.parse("251 Mercer St., New York, NY, 10003"))
#returns {'suite_type': None, 'other': 'New York NY 10003', 'house': '251', 'street_name': 'Mercer', 'street_type': 'St', 'suite_num': None, 'street_full': 'Mercer St'}
```

As you can see we have a nice representation of the street number, street name, street type, and the full street.  Let's see what happens when we try messing around with the ordering:

```
# .. same code as above ..
print(addr_parser.parse("New York, NY, 10003, 251 Mercer St."))
#returns {'suite_type': None, 'other': None, 'house': None, 'street_name': 'New York NY 10003 251 Mercer', 'street_type': 'St', 'suite_num': None, 'street_full': 'New York NY 10003 251 Mercer St'}
```

Okay, so streetaddress kind of falls apart for addresses that aren't well formatted.  So can we do better?  

Enter usaddress - 

`pip install usaddress`

```
 import usaddress
usaddress.parse("251 Mercer St. New York, NY, 10003")
#return [('251', 'AddressNumber'), ('Mercer', 'StreetName'), ('St.', 'StreetNamePostType'), ('New', 'PlaceName'), ('York,', 'PlaceName'), ('NY,', 'StateName'), ('10003', 'ZipCode')]
```

This seems promising!  We get the zip code, state name, the place name is a little awkward, but it's not too bad.  

Let's mess around a little :D

```
usaddress.parse("New York, NY, 10003, 251 Mercer St.")
#returns [('New', 'PlaceName'), ('York,', 'PlaceName'), ('NY,', 'StateName'), ('10003,', 'ZipCode'), ('251', 'AddressNumber'), ('Mercer', 'StreetName'), ('St.', 'StreetNamePostType')]
```

Oh wow!  It works!  ;)  

As you can see, usaddress handles poorly formed addresses (specifically ones out of order) extremely well.  It's slightly annoying that it returns a list of tuples, but w/e it discerns the semantic information, very very well.  Which is the major challenge with address parsing.  

At this point we have the semantic parsing complete, now we need a tool to get lat/long coordinates from a well formed address.  And if the address is poorly formed, we can make it well formed with the semantic parser we defined above!





###Parsing Phone number information
