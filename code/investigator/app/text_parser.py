"""
This code is used to pull hard attributes out of text from backpage ads and other services related to trafficking

it has 70% test coverage - in tests.py

tested functions:

letter_to_number
phone_number_parse

untested functions:

verify_phone_number
"""
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


