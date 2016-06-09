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
    
    parameters:
    @number - a string representation of a set of digits
    """
    data = pickle.load(open("twilio.creds","r"))
    r = requests.get("http://lookups.twilio.com/v1/PhoneNumbers/"+number,auth=data)
    if "status_code" in json.loads(r.content).keys():
        return False
    else:
        return True

#two competiting implementations of grabbing phone numbers from text
def phone_number_grab(text):
    """
    pulls phone numbers out of structured text
    
    parameter:
    @text - string of unstructured text
    """
    phone_numbers = []
    text = letter_to_number(text)
    tmp_phone = []
    for ind,letter in enumerate(text):
        if letter.isdigit():
            tmp_phone.append(letter)
        if len(tmp_phone) == 10 and phone[0] != '1':
            if verify_phone_number(''.join(tmp_phone)):
                phone_numbers.append(''.join(tmp_phone))
        elif len(tmp_phone) == 11 and phone[0] != '1':
            if verify_phone_number(''.join(tmp_phone)):
                phone_numbers.append(''.join(tmp_phone))
    return phone_numbers
    
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
    for ind,letter in enumerate(text):
        if letter.isdigit():
            phone.append(letter)
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
        for number in possible_numbers:
            if verify_phone_number(number):
                phone_numbers.append(number)
    return phone_numbers
