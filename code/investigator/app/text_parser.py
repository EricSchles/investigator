def letter_to_number(self,text):
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

    def verify_phone_number(self,number):
        #I know this worked at some point...test this on other computer
        data = pickle.load(open("twilio.creds","r"))
        r = requests.get("http://lookups.twilio.com/v1/PhoneNumbers/"+number,auth=data)
        if "status_code" in json.loads(r.content).keys():
            return False
        else:
            return True
        
    def phone_number_parse(self,values):
        phone_numbers = []
        text = self.letter_to_number(values["text_body"])
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
            if self.verify_phone_number(number):
                phone_numbers.append(number)
        return phone_numbers
