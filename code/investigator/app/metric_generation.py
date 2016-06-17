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
from app.models import Backpage,BackpageAdInfo
from datetime import datetime

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
def _prepare_for_month_over_month_timeseries(datetimes,frequencies):
    year_months = []
    x_vals = []
    y_vals = []
    summation = 0
    for ind,date in enumerate(datetimes):
        summation += frequencies[ind]
        if not (date.year,date.month) in year_months:
            year_months.append((date.year,date.month))
            x_vals.append(datetime(year=date.year,month=date.month,day=date.day))
            y_vals.append(summation)
            summation = 0
    return x_vals,y_vals

def get_locations():
    list_of_ads = BackpageAdInfo.query.all()
    return [[ad.longitude,ad.latitude] for ad in list_of_ads if ad.latitude != 'no address information' and ad.longitude !='no address information' and ad.latitude and ad.longitude]
    
def _prepare_for_unique_month_over_month_timeseries(datetimes):
    year_months = []
    x_vals = []
    y_vals = []
    summation = 0
    for ind,date in enumerate(datetimes):
        summation += 1
        if not (date.year,date.month) in year_months:
            year_months.append((date.year,date.month))
            x_vals.append(datetime(year=date.year,month=date.month,day=date.day))
            y_vals.append(summation)
            summation = 0
    return x_vals,y_vals

def overall_number_of_posts_in_adults_month_over_month():
    list_of_ads = Backpage.query.all()
    datetimes = [elem.timestamp for elem in list_of_ads]
    month_over_month_frequencies = _prepare_for_unique_month_over_month_timeseries(datetimes)
    return month_over_month_frequencies

def unique_posts_per_hour_day_of_the_week():
    datetimes = get_unique_ads()
    hour_over_hour_frequencies = _prepare_for_unique_hour_over_hour_timeseries(datetimes)
    return hour_over_hour_frequencies

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
    
def overall_number_of_unique_posts_in_adults_month_over_month():
    datetimes = get_unique_ads()
    month_over_month_frequencies = _prepare_for_unique_month_over_month_timeseries(datetimes)
    return month_over_month_frequencies


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

def parse_number(phone_numbers):
    if phone_numbers == None:
        return phone_numbers
    if "{" in phone_numbers and "}" in phone_numbers:
        phone_numbers = phone_numbers.strip("{").strip("}")
        return phone_numbers.split(",")
    else:
        return phone_numbers
