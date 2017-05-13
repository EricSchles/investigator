from app import text_parser,metric_generation,tools
from app.geographic_processing import contains
from num2words import num2words
from datetime import datetime
import random

"""
Regarding these tests:

It is worth noting that all phone_number_parse tests require a connection to the internet, as well as twilio credentials.  If you haven't added a twilio account, these tests will not work.

"""

def test_contains():
    point_to_check = (40.77264, -73.7471156)
    box = [(40.775329,-73.753134),
           (40.777100, -73.746568),
           (40.768537, -73.741225),
           (40.767740,-73.751504)]

    assert contains(xs,ys,point_to_check) == True

#tests for tools
def test_generate_connected_graph():
    listing = ["a","b","c","d"]
    assert {"a":["b","c","d"],"b":["c","d"],"c":["d"],"d":[]} == tools.generate_connected_graph(listing)

#tests for text_parser
def test_letter_to_number():
    words = [num2words(elem) for elem in list(range(10))] 
    assert all([text_parser.letter_to_number(word).isdigit() for word in words])
    
def test_first_phone_number_parse():
    text = """
    Hi th5e1r6e sevEN sEvEn I'm brandi
    thRee and I'4m071 looking for a good time :)
    """
    assert "5167734071" == text_parser.phone_number_parse(text)

def test_second_phone_number_parse():
    text = """
    Hi there 516SevensEVENThree40SeVen1 is my number.  Give me a call!
    """
    assert "5167734071" == text_parser.phone_number_parse(text)

def test_third_phone_number_parse():
    text = """
    Hi there I'm brandi I'm a 23 yr old and I'm super hot. 516SevensEVENThree40SeVen1 is my number.  Give me a call!
    """
    print(text_parser.phone_number_parse(text))
    assert "5167734071" == text_parser.phone_number_parse(text)


#tests for metric_generation
def test_first__prepare_for_hour_over_hour_timeseries():
    datetimes = [datetime(year=random.randint(2007,2015),month=random.randint(1,12),day=random.randint(1,28))
                 for _ in range(20)]
    frequencies = [random.randint(0,300) for _ in range(20)]
    assert type(metric_generation._prepare_for_hour_over_hour_timeseries(datetimes,frequencies)) == type(dict())

def test_second__prepare_for_hour_over_hour_timeseries():
    datetimes = []
    for hour in range(0,24):
        for day in range(1,15):
            datetimes.append(datetime(year=2016,month=1,day=day,hour=hour))
    keys = [(elem.strftime("%A"),elem.hour) for elem in datetimes]
    dicter = {}.fromkeys(keys,random.randint(0,300))
    frequencies = [dicter[elem] for elem in keys]
    assert dicter == metric_generation._prepare_for_hour_over_hour_timeseries(datetimes,frequencies)
