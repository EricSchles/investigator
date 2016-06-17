"""
This code is used to pull hard attributes out of text from backpage ads and other services related to trafficking

it has 25% test coverage - in tests.py

tested functions:

letter_to_number
phone_number_parse

untested functions:

verify_phone_number
address_is_complete
get_streetnames
get_lat_long
format_address
format_streetname_post_type

"""
#for phone number parsing
import pickle
import requests
import json

#for address parsing
import usaddress
from geopy.geocoders import Nominatim, GoogleV3

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
            #phone = phone[1:]
            phone = []
        if len(phone) == 11 and phone[0] == '1':
            possible_numbers.append(''.join(phone))
            #phone = phone[1:]
            phone = []
    if not any([len(elem) == 10 or len(elem) == 11 for elem in  possible_numbers]):
        possible_numbers += [''.join(total_number_array)]
    for number in possible_numbers:
        if verify_phone_number(number):
            phone_numbers.append(number)
    if len(phone_numbers) == 1:
        return phone_numbers[0]
    return phone_numbers

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
    streetnames = []
    parsed_text = usaddress.parse(text)
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
        google_encoder = GoogleV3(google_api_key)
        parsed_text = address_is_complete(text)
        if parsed_text == "complete":
            location = google_encoder.geocode(text)
        elif parsed_text == "cross street":
            location = google_encoder.geocode(' and '.join(get_streetnames(text)) + place)
        elif parsed_text == 'no address information':
            return "no address information","no address information"
    if location:
        return location.latitude, location.longitude
    else:
        return "no address information","no address information"
    
def clean_location_string(text):
    return text.replace("&"," ").replace("\r"," ").replace("\n"," ").replace("Location:","").replace("•","").strip()

def strip_post_id(text):
    return text.split(": ")[1].split(" ")[0]
