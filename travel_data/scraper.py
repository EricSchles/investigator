import requests
import lxml.html
from geopy.geocoders import Nominatim, GoogleV3

def to_dict(listing):
    dicter = {}
    for elem in listing:
        if elem.count("(") > 1:
            split_index = elem.rfind("(")
            name = elem[:split_index]
            abbr = elem[split_index+1:]
        else:
            name, abbr = elem.split("(")
        abbr = abbr.replace(")","")
        dicter[abbr] = name
    return dicter

airport_codes = requests.get("http://www.airportcodes.org/").text
airport_html = lxml.html.fromstring(airport_codes)
result = airport_html.xpath("//table")
airports = result[2].text_content()
airport_list = [elem for elem in airports.split("\n") if not elem == '']
airport_list = [elem for elem in airport_list if elem != '\t']
airport_list = [elem for elem in airport_list if "(" in elem]
airport_mapping = to_dict(airport_list)

nominatim_encoder = Nominatim()
#location = nominatim_encoder.geocode(formatted_text)

airport_to_latlong = {abbr:nominatim_encoder.geocode(airport_mapping[abbr]) for abbr in airport_mapping}

