#This file will have a set of classes used throughout the program

#Imports for ParsePhoneNumber
import json
import pickle
import requests

#Imports for ParseAddress
import usaddress
from streetaddress import StreetAddressFormatter
from nltk.tag.stanford import StanfordNERTagger as Tagger
from geopy.geocoders import GoogleV3,Nominatim
import nltk
import geopy

tagger = Tagger('/opt/stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz','/opt/stanford-ner-2014-08-27/stanford-ner.jar')

addr_formatter = StreetAddressFormatter()

#a queue for storing processes
class Queue:
    def __init__(self):
        self.internal_list = []
    def put(self,data):
        self.internal_list.append(data)
    def get(self):
        if self.internal_list != []:
            data = self.internal_list[0]
            del self.internal_list[0]
            return data
        else:
            return None
#Consider having a generalized parse method for each of these objects
class ParsePhoneNumber:
        
    #text is a string
    def _letter_to_number(self,text):
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

    #number is a string
    #twilio creds is a tuple (auth_id,auth_key)
    def _verify_phone_number(self,number):
        #I know this worked at some point...test this on other computer
        data = pickle.load(open("twilio.creds","r"))
        r = requests.get("http://lookups.twilio.com/v1/PhoneNumbers/"+number,auth=data)
        if "status_code" in json.loads(r.content).keys():
            return False
        else:
            return True
        
    #values is a dictionary
    def phone_number_parse(self,values):
        phone_numbers = []
        text = self._letter_to_number(values["text_body"])
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
            if self._verify_phone_number(number):
                phone_numbers.append(number)
        return phone_numbers


class ParseAddress:
    #If we are pulling this information from an excel document then we'll likely have the address information in an acceptable form
    #Otherwise we'll need to run the text through usaddress or streetaddress
    def __init__(self,from_api=False,from_excel=False):
        self.from_api = from_api
        self.from_excel = from_excel

    def pre_formatter(self,addr,dict_addr):
        if "StreetNamePostType" in dict_addr.keys():
            addr = addr.replace("St","Street")
            addr = addr.replace("St.","Street")
            addr = addr.replace("st","Street")
            addr = addr.replace("st.","street")
        return addr
        
    #The parse will get you a lat/long representation of the address, which exists somewhere in the passed in text.
    #It expects free form text or a complete address
    def parse(self,text,place="NYC"):
        dict_addr,addr_type = self.preprocess(text)
        google_key = pickle.load(open("google_api_key.pickle","r"))
        g_coder = GoogleV3(google_key)
        if addr_type == 'complete':
            combined_addr = []
            keys = ["AddressNumber","StreetName","StreetNamePostType","PlaceName","StateName","ZipCode"]
            for key in keys:
                try:
                    combined_addr += [dict_addr[key]]
                except KeyError:
                    continue
                addr = " ".join(combined_addr) 
            n_coder = Nominatim()
            addr = self.pre_formatter(addr,dict_addr)
            lat_long = n_coder.geocode(addr)
            if lat_long: #means the request succeeded
                return lat_long
            else:
                lat_long = g_coder.geocode(addr)
                return lat_long
            #If None, means no address was recovered.
        if addr_type == 'cross streets':
            cross_addr = " and ".join(dict_addr) + place 
            try:
                lat_long = g_coder.geocode(cross_addr)
                return lat_long
            except geopy.geocoders.googlev3.GeocoderQueryError:
                return None
        
    #remove near, split on commas, 
    #tag - div style="padding-left:2em;
    #two possible return "types" - complete a real address or cross streets, which only gives two cross streets and therefore an approximate area
    def preprocess(self,text):
        #this case is included because usaddress doesn't do a great job if there isn't a number at parsing semantic information
        #However if there is a number it tends to be better than streetaddress
        #Therefore usaddress is better at figuring out where the start of an address is, in say a very long body of text with an address in there at some point
        #It isn't that great at approximate locations
        nouns = ['NN','NNP','NNPS','NNS']
        if any([elem.isdigit() for elem in text.split(" ")]):
            addr = usaddress.parse(text)
            addr = [elem for elem in addr if elem[1] != 'Recipient']
            addr_dict = {}
            for value,key in addr:
                if key in addr_dict.keys():
                    addr_dict[key] += " "+value
                else:
                    addr_dict[key] = value
            return addr_dict,"complete"
        else:
            possible_streets = []
            for word,tag in tagger.tag(text.split()):
                if tag == 'LOCATION':
                    possible_streets.append(word)
            parts = nltk.pos_tag(nltk.word_tokenize(text))
            for part in parts:
                if any([part[1]==noun for noun in nouns]):
                    possible_streets.append(part[0])
            return possible_streets,"cross streets"

        #addresses: http://stackoverflow.com/questions/11160192/how-to-parse-freeform-street-postal-address-out-of-text-and-into-components
        #To do: build general list from http://www.nyc.gov/html/dcp/html/bytes/dwnlion.shtml
        #And from https://gis.nyc.gov/gisdata/inventories/details.cfm?DSID=932
        
        #Here I need to add Part of Speech tagging and pull out all the nouns as possible street names.
        #Then I need to come up with a list of street names in NYC and run each noun through the list
        #From there I'll have all the street names
            


