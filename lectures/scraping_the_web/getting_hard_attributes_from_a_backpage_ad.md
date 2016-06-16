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

All our examples will come from geopy - to get it open a command line and type:

`pip install geopy`

The geopy library is amazing!  It has lots of utilities for doing things with geographic data.  We'll be making use of it's geocoders api.  A geocoder is way of taking an address in and returning a latitude/longitude coordinate for that address.  The geopy library comes with lots of different geocoders, we'll be making use of a few of them.  First let's look at Nominatim (because it's free as in beer).  You can see [the docs for geopy here](https://geopy.readthedocs.io/en/1.10.0/).

```
>>> from geopy.geocoders import Nominatim
>>> encoder = Nominatim()
>>> location = encoder.geocode("251 Mercer Street, New York, NY, 10003")
>>> location

Location(NYU Courant Institute of Mathematical Sciences, 251, Mercer Street, Washington Square Village, Manhattan, New York County, NYC, New York, 10012, United States of America, (40.7286994, -73.995715, 0.0))

>>> dir(location)

['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__unicode__', '_address', '_point', '_raw', '_tuple', 'address', 'altitude', 'latitude', 'longitude', 'point', 'raw']
```

As you can see, we get back a Location object with lots and lots of great information, among other things, the latitude/longitude.  We can access the latitude and longitude by calling:

```
>>> location.latitude
>>> location.longitude
```

This tends to work pretty well when you have well formed addresses.  So now let's put together our two components to get our latitude / longitude.

First we'll need some utility functions to ensure our address appears in the correct form:

```
import usaddress
from geopy.geocoders import Nominatim

def format_streetname_post_type(post_type):
    if post_type.lower() == "st.":
        return "Street"
    elif post_type.lower() == "ct." or post_type.lower() == 'crt.':
        return "Court"
    else:
    	return post_type

def format_address(addr):
    addr_components = usaddress.parse(addr)
    dicter = {}
    for component in addr_components:
        if not component[1] in dicter.keys():
            dicter[component[1]] = component[0]
        else:
            dicter[component[1]] += " "+component[0]
    return dicter["AddressNumber"] + " " + dicter["StreetName"] + " " + dicter["StreetNamePostType"] + " " + dicter["PlaceName"] + " " + dicter["StateName"] + " "+ dicter["ZipCode"]

encoder = Nominatim()
location = encoder.geocode(format_address("251 Mercer St. , New York, NY,  10003"))
print(location.latitude)
print(location.longitude)
```

Now we are guaranteed, assuming we only get an address, we will be able to get back the latitude / longitude.  What happens when we get more than an address?  Like an address inside of "unstructured text"?

```
#... snip from last piece of code ...
>>> location = encoder.geocode(format_address("Hello my name is Eric and I went to school at NYU, specifically:  251 Mercer St. , New York, NY,  10003"))
>>> location
Location(NYU Courant Institute of Mathematical Sciences, 251, Mercer Street, Washington Square Village, Manhattan, New York County, NYC, New York, 10012, United States of America, (40.7286994, -73.995715, 0.0))
```

Holy smokes!  We got the same information, given an address embedded in free form text!  So, we can get the address information if it's not in the correct order AND if it's among other pieces of text we don't care about.  

Okay, so can we do better? Well, what does better mean at this point?  For me, it means handling addresses with missing information, and still getting an approximation of a precise location.  

The first thing we'll do is get a relative address, without zipcode, or exact street address.  To do this, we'll make use of google's geoencoder, which is totally bad ass!  It can handle cross streets, no zip code, and a bunch more craziness.

This will add another layer of complexity - we'll need key's to use google's geoencoder.  But the nice thing is, we can still use geopy to actually make our calls.

Getting an api key for address lookups from google isn't too bad.  There's a little bit more search required within their documentation than I would like, but whatever.

If you're generally interested in maps check out [this page](https://developers.google.com/maps/)
Here's some documentation for the [geoencoder api](https://developers.google.com/maps/documentation/geocoding/start).

And finally, here's the documentation on creating a [google geoencoder api](https://developers.google.com/maps/documentation/geocoding/start#get-a-key).

We'll be clicking on the "GET A KEY" button:

![](pictures/get_api_key_google.png)

We'll click continue on this screen ("create a new project"):

![](pictures/create_a_new_project_google.png)

Now we'll name our project investigator (feel free to name this whatever you want).

![](pictures/project_name_google.png)

On the next screen, you'll see an api key - unfortunately I can't show you that screen without showing you my api key.  Copy the key and doing the following from a python repl:

```
>>> import pickle
>>> api_key="Your API KEY goes here"
>>> pickle.dump(api_key,open("google_geocoder_api.creds","wb"))
```

If you are using github it's worth noting that my .gitignore has `*.creds`, if you don't like that extension for whatever reason, feel free to choose your own adventure for your credentials extension :)

Okay, so now that we went through those extra steps, let's check out the pay off:

```
>>> from geopy.geocoders import GoogleV3
>>> import pickle
>>> api_key = pickle.load(open("google_geocoder_api.creds","rb"))
>>> encoder = GoogleV3(api_key)
>>> encoder.geocode("14th street and 5th ave., New York, NY")
Location(5th Ave & W 14th St, New York, NY 10011, USA, (40.7360158, -73.9936331, 0.0))
```

WOW.  Google - the tech is strong with you.  Okay, so let's see what happens when we put in free form text, do we even need to format things with `usaddress` now?

```
#... snipped from the previous piece of code
>>> encoder.geocode("Hello my name is Eric and I want to go to 14th street and 5th ave., New York, NY")
Location(5th Ave, New York, NY, USA, (40.774734, -73.96538439999999, 0.0))
```

Okay, so google doesn't do terribly, but also not as good.  But no fear!  usaddress to the rescue!  Turns out we can get multiple addresses out of usaddress, no problem!!

```
import usaddress
>>> usaddress.parse("I'm at the corner of Lexington and 51 st.")
[("I'm", 'Recipient'), ('at', 'Recipient'), ('the', 'Recipient'), ('corner', 'Recipient'), ('of', 'AddressNumber'), ('Lexington', 'StreetName'), ('and', 'StreetName'), ('51', 'StreetName'), ('st.', 'StreetNamePostType')]
```

So to make use of relative locations all we need to do is:

```
parsed_text = usaddress.parse("I'm at the corner of Lexington and 51 st."))
for ind,word in enumerate(parsed_text):
     if word[1] == "StreetName":
             if word[0] not in ["and","or","near","between"]:
                     if ind+1 < len(parsed_text):
                             if parsed_text[ind+1][1] == "StreetNamePostType": 
                                     streetnames.append(word[0]+ " " + parsed_text[ind+1][0])
                             else:
                                     streetnames.append(word[0])
                     else:
                             streetnames.append(word[0])
>>> streetnames
['Lexington', '51 st.'] 
```

And then we can pass street ' and '.join(streetnames) + place to google!

Here's our finished functions for parsing address information:

```
import pickle
import requests
import json
import usaddress
from geopy.geocoders import Nominatim, GoogleV3

def format_streetname_post_type(post_type):
    if post_type.lower() == "st.":
        return "Street"
    elif post_type.lower() == "ct." or post_type.lower() == 'crt.':
        return "Court"
    else:
        return post_type
    
def format_address(addr):
    addr_components = usaddress.parse(addr)
    dicter = {}
    for component in addr_components:
        if not component[1] in dicter.keys():
            dicter[component[1]] = component[0]
        else:
            dicter[component[1]] += " "+component[0]
    return dicter["AddressNumber"] + " " + dicter["StreetName"] + " " + format_streetname_post_type(dicter["StreetNamePostType"]) + " " + dicter["PlaceName"] + " " + dicter["StateName"] + " "+ dicter["ZipCode"]

def address_is_complete(text):
    streetname_exists = False
    streetnumber_exists = False
    cross_street = False
    num_streets = 0
    for elem in usaddress.parse(text):
        if "StreetName" == elem[1]:
            streetname_exists = True
            num_streets += 1
        if "AddressNumber" == elem[1] and elem[1].isdigit():
            streetnumber_exists = True
    if streetname_exists and streetnumber_exists:
        return "complete"
    elif num_streets > 1 and not streetnumber_exists:
        return "cross street"
    else:
        return "no address information"

def get_streetnames(text):
    parsed_text = usaddress.parse("I'm at the corner of Lexington and 51 st."))
    for ind,word in enumerate(parsed_text):
        if word[1] == "StreetName":
            if word[0] not in ["and","or","near","between"]:
                if ind+1 < len(parsed_text):
                    if parsed_text[ind+1][1] == "StreetNamePostType": 
                        streetnames.append(word[0]+ " " + parsed_text[ind+1][0])
                    else:
                        streetnames.append(word[0])
                else:
                    streetnames.append(word[0])
    return streetnames

def get_lat_long(text,place):
    try:
        formatted_text = format_address(text)
        nominatim_encoder = Nominatim()
        location = nominatim_encoder.geocode(formatted_text)
    except:
        google_api_key = pickle.load(open("google_geocoder_api.creds","rb"))
        google_encoder = GoogleV3(api_key)
        parsed_text = address_is_complete(text)
        if parsed_text == "complete":
            location = google_encoder(text)
        elif parsed_text == "cross street":
            location = google_encoder(' and '.join(get_streetnames(text)) + place)
        elif parsed_text == 'no address information':
            return "no address information"
    return location.latitude, location.longitude
```

###Parsing Phone number information

Parsing phone numbers from unstructured text is a very hard job.  It took close to a year to get this rule based algorithm to work, "well enough".  Where well enough is around 80-90% of the time.  I'm going to leave the explanation for this section as a stub as all the important work has already been done.  Here's the code:

```

import pickle
import requests
import json

def letter_to_number(text):
    """
    This little function simply turns word representations to digit representations of numbers.

    parameters:
    @text - a string of "unstructured" text, that we are going to process.
    """
    text= text.upper()
    text = text.replace("ONE","1")
    text = text.replace("TWO","2")
    text = text.replace("THREE","3")
    text = text.replace("FOUR","4")
    text = text.replace("FIVE","5")
    text = text.replace("SIX","6")
    text = text.replace("SEVEN","7")
    text = text.replace("EIGHT","8")
    text = text.replace("NINE","9")
    text = text.replace("ZERO","0")
    return text

def verify_phone_number(number):
    """
    verify phone number leverages the twilio api to verify the phone number actually corresponds to an active number.
    The twilio api for this: https://www.twilio.com/docs/api/lookups
    
    parameters:
    @number - a string representation of a set of digits
    """
    data = pickle.load(open("twilio.creds","rb"))
    r = requests.get("http://lookups.twilio.com/v1/PhoneNumbers/"+number,auth=data)
    if "status_code" in json.loads(r.content.decode("ascii")).keys():
        return False
    else:
        return True

def phone_number_parse(text):
    """
    pulls phone numbers out of structured text
    
    parameter:
    @text - string of unstructured text
    """
    phone_numbers = []
    text = letter_to_number(text)
    phone = []
    counter = 0
    found = False
    possible_numbers = []
    total_number_array = []
    for ind,letter in enumerate(text):
        if letter.isdigit():
            phone.append(letter)
            total_number_array.append(letter)
            found = True
        else:
            if found:
                counter += 1
            if counter > 15 and found:
                phone = []
                counter = 0
                found = False
            #country codes can be two,three digits
        if len(phone) == 10 and phone[0] != '1':
            possible_numbers.append(''.join(phone))
            phone = phone[1:]
        if len(phone) == 11 and phone[0] == '1':
            possible_numbers.append(''.join(phone))
            phone = phone[1:]
    if not any([len(elem) == 10 or len(elem) == 11 for elem in  possible_numbers]):
        possible_numbers += [''.join(total_number_array)]
    for number in possible_numbers:
        if verify_phone_number(number):
            phone_numbers.append(number)
    if len(phone_numbers) == 1:
        return phone_numbers[0]
    return phone_numbers
```

