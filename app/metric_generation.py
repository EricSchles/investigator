"""
This module prepares different metrics for data visualization it is used in visualize_metrics

test coverage:

presently there is 25% test coverage in tests.py

covered methods:
_prepare_for_hour_over_hour_timeseries

uncovered methods:
number_of_posts_in_adults_hour_over_hour
_prepare_for_month_over_month_timeseries
overall_number_of_posts_in_adults_month_over_month
"""
from app.models import Backpage, BackpageAdInfo, AreaCodeLookup
from datetime import datetime
from app.nlp_tools import phrase_frequency,document_similarity,phrase_frequency_ads
from app.tools import generate_connected_graph

import time

#text processing
def overall_comparison():
    total_ads = [elem.ad_body for elem in BackpageAdInfo.query.all()]
    return phrase_frequency(total_ads)

def phrase_frequency_categorized_by_phone_number():
    ads = {}
    for ad in BackpageAdInfo.query.all():
        if ad.phone_number and (len(ad.phone_number) == 10 or len(ad.phone_number) == 11):
            if ad.phone_number in ads:
                ads[ad.phone_number] += "\n" + ad.ad_body
            else:
                ads[ad.phone_number] = ad.ad_body
    phrase_frequency_per_phone_number = {}
    for ad in ads.keys():
        phrase_frequency_per_phone_number[ad] = phrase_frequency_ads(ads[ad])
    return phrase_frequency_per_phone_number

def average_phrase_similarity_between_documents_by_phone_number(number_of_grams=10,profiling=False):
    ads = {}
    for ad in BackpageAdInfo.query.all():
        if ad.phone_number and (len(ad.phone_number) == 10 or len(ad.phone_number) == 11):
            if ad.phone_number in ads:
                ads[ad.phone_number] += "\n" + ad.ad_body
            else:
                ads[ad.phone_number] = ad.ad_body
    checklist_of_nodes_to_process = generate_connected_graph([key for key in ads.keys()])
    average_per_gram = {}.fromkeys([elem for elem in range(1,number_of_grams)],0)
    total = 0
    
    for key in checklist_of_nodes_to_process:
        if profiling:
            print(len(checklist_of_nodes_to_process[key]),"total nodes to process")
        if profiling: start = time.time()
        for list_item in checklist_of_nodes_to_process[key]:
            similarity_scores = document_similarity(ads[key],ads[list_item])
            total += 1
            for i_gram in similarity_scores.keys():
                average_per_gram[i_gram] += similarity_scores[i_gram]
        if profiling: print(time.time() - start)
    average_per_gram = {key:average_per_gram[key]/total for key in average_per_gram.keys()}
    return average_per_gram

#Hour over Hour analysis - corresponds to metrics of type 2 subtype 1 in lectures/scraping_the_web.md
def _prepare_for_hour_over_hour_timeseries(datetimes,frequencies):
    day_hours = {}
    for ind,time_obj in enumerate(datetimes):
        day = time_obj.strftime("%A")
        hour = time_obj.hour
        if not (day,hour) in day_hours.keys():
            day_hours[(day,hour)] = frequencies[ind]
        else:
            day_hours[(day,hour)] = day_hours[(day,hour)] + (1/ind*(frequencies[ind] - day_hours[(day,hour)]))
    return day_hours

def number_of_posts_in_adults_hour_over_hour():
    list_of_ads = Backpage.query.all()
    datetimes = [elem.timestamp for elem in list_of_ads]
    frequencies = [elem.frequency for elem in list_of_ads]
    hour_over_hour_frequencies = _prepare_for_hour_over_hour_timeseries(datetimes,frequencies)
    return hour_over_hour_frequencies

#Month over Month analysis - corresponds to metrics of type 2 subtype 2 in lectures/scraping_the_web.md
def overall_number_of_posts_in_adults_month_over_month():
    list_of_ads = Backpage.query.all()
    datetimes = [elem.timestamp for elem in list_of_ads]
    frequencies = [elem.frequency for elem in list_of_ads]
    month_over_month_frequencies = _prepare_for_month_over_month_timeseries(datetimes,frequencies)
    return month_over_month_frequencies

def _prepare_for_month_over_month_timeseries(datetimes,frequencies):
    year_months = []
    x_vals = []
    y_vals = []
    for date in datetimes:
        if not (date.year,date.month) in year_months:
            cur_year = date.year
            cur_month = date.month
            year_months.append((date.year,date.month))
            x_vals.append(datetime(year=date.year,month=date.month,day=date.day))
            y_vals.append(sum([frequencies[index] for index,elem in enumerate(datetimes) if elem.year==cur_year and elem.month==cur_month]))
    return x_vals,y_vals

#Unique versions of the above metrics
def overall_number_of_unique_posts_in_adults_month_over_month():
    datetimes = get_unique_ads()
    month_over_month_frequencies = _prepare_for_unique_month_over_month_timeseries(datetimes)
    return month_over_month_frequencies

def _prepare_for_unique_month_over_month_timeseries(datetimes):
    year_months = []
    x_vals = []
    y_vals = []
    for ind,date in enumerate(datetimes):
        if not (date.year,date.month) in year_months:
            cur_year = date.year
            cur_month = date.month
            year_months.append((date.year,date.month))
            x_vals.append(datetime(year=date.year,month=date.month,day=date.day))
            y_vals.append(len([datetime for datetime in datetimes if datetime.year==cur_year and datetime.month==cur_month]))
    return x_vals,y_vals

def unique_posts_per_hour_day_of_the_week():
    datetimes = get_unique_ads()
    hour_over_hour_frequencies = _prepare_for_unique_hour_over_hour_timeseries(datetimes)
    return hour_over_hour_frequencies

def _prepare_for_unique_hour_over_hour_timeseries(datetimes):
    day_hours = {}
    for ind,time_obj in enumerate(datetimes):
        day = time_obj.strftime("%A")
        hour = time_obj.hour
        if not (day,hour) in day_hours.keys():
            day_hours[(day,hour)] = 1
        else:
            day_hours[(day,hour)] += 1 
    return day_hours

def get_unique_ads():
    seen_phone_numbers = []
    list_of_ads = BackpageAdInfo.query.all()
    unique_ads = []
    for ad in list_of_ads:
        parsed_number = parse_number(ad.phone_number)
        if parsed_number == None: continue
        if len(parsed_number) > 1:
            if len([number for number in parsed_number if number not in seen_phone_numbers]) == len(parsed_number):
                seen_phone_numbers += parsed_number
                unique_ads.append(ad)
        else:
            if parsed_number not in seen_phone_numbers:
                unique_ads.append(ad)
                seen_phone_numbers.append(parsed_number)
    return [elem.timestamp for elem in unique_ads if elem.timestamp]

def parse_number(phone_numbers):
    if phone_numbers == None:
        return phone_numbers
    if "{" in phone_numbers and "}" in phone_numbers:
        phone_numbers = phone_numbers.strip("{").strip("}")
        return phone_numbers.split(",")
    else:
        return phone_numbers

def get_locations():
    list_of_ads = BackpageAdInfo.query.all()
    return [[ad.longitude,ad.latitude] for ad in list_of_ads if ad.latitude != 'no address information' and ad.longitude !='no address information' and ad.latitude and ad.longitude]

def get_area_code_locations():
    area_codes = AreaCodeLookup.query.all()
    return [[area_code.longitude, area_code.latitude] for area_code in area_codes if area_code.latitude != 'no address information' and area_code.longitude !='no address information' and area_code.latitude and area_code.longitude]
