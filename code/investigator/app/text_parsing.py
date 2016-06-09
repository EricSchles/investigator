import pickle
import requests

def letter_to_number(text):
    """
    letter_to_number turns written numbers to there digit representation

    @text - string, the ad body text from a backpage ad.
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
    This simple function calls the twilio lookup api.  The twilio.creds is a user,password combination.
    For more info on twilio look ups check out: [TODO FILL THIS IN]
    Here we use this simple function in the most naive way, simply verifying that our phone number is 
    an actual number.
    
    parameters:
    @number - a string phone number to verify
    """
    data = pickle.load(open("twilio.creds","r"))
    r = requests.get("http://lookups.twilio.com/v1/PhoneNumbers/"+number,auth=data)
    if "status_code" in json.loads(r.content).keys():
        return False
    else:
        return True
        
def phone_number_parse(text):
    """
    phone number parse parses for phone numbers in unstructured text.
    
    parameters:
    @text - a string from a backpage ad, or other piece of text
    
    """
    possible_phone_numbers = []
    text = letter_to_number(ad_body)
    tmp_number = []
    for ind,letter in enumerate(text):
        if letter.isdigit():
            tmp_number.append(letter)
        if len(tmp_number) == 10 and tmp_number[0] != '1':
            possible_phone_numbers.append(tmp_number)
            tmp_number = []
        if len(tmp_number) == 11 and tmp_number[0] == '1':
            possible_phone_numbers.append(tmp_number)
            tmp_number = []
    return possible_phone_numbers
    for number in possible_phone_numbers:
        if verify_phone_number(number):
            return number
