"""

This module holds all the code for directly visualizing our metrics.  We can think of it as a main work horse in our
set of tools around understanding the human trafficking space.  It should be noted that there will be work on creating textual descriptions as well as visual.

test_coverage:

0% - this will be rememdied soon
"""
from app import metric_generation
import shutil
from collections import OrderedDict
import pandas as pd
import plotly
from plotly.graph_objs import Bar,Layout,Scatter, Box, Annotation,Marker,Font,XAxis,YAxis
import scipy as sp
from scipy.stats import describe
from datetime import datetime
import numpy as np
from statsmodels.api import formula 
import plotly
import scipy as sp
from scipy.stats import describe
import code
import shutil
from num2words import num2words

def plot_simple_timeseries(dates,frequencies,filename):
    x_vals = dates
    y_vals = frequencies
        
    plotly.offline.plot({
        "data":[Scatter(x=x_vals,y=y_vals)],
        "layout":Layout(
            title="Time Series analysis of backpage escort section"
        )
    },auto_open=False)
    shutil.move("temp-plot.html",filename)

def visualize_unique_month_over_month():
    months,frequencies = metric_generation.overall_number_of_unique_posts_in_adults_month_over_month()
    plot_simple_timeseries(months,frequencies,"app/templates/unique_backpage_month_over_month_frequencies.html")

def visualize_month_over_month():
    months,frequencies = metric_generation.overall_number_of_posts_in_adults_month_over_month()
    plot_simple_timeseries(months,frequencies,"app/templates/backpage_month_over_month_frequencies.html")

def order_day_hour(vals):
    dicter = OrderedDict({})
    dicter["Monday"] = []
    dicter["Tuesday"] = []
    dicter["Wednesday"] = []
    dicter["Thursday"] = []
    dicter["Friday"] = []
    dicter["Saturday"] = []
    dicter["Sunday"] = []
    for val in vals:
        dicter[val[0]].append(val)
    for day in dicter.keys():
        dicter[day] = sorted(dicter[day], key=lambda t:t[1])
    x_vals = []
    for key in dicter.keys():
        x_vals += dicter[key]
    return x_vals
    
def plot_simple_barchart(time_freq,filename):
    time_freq = OrderedDict(time_freq)
    x_vals = [elem for elem in time_freq.keys()]
    x_vals = order_day_hour(x_vals)
    y_vals = [time_freq[elem] for elem in x_vals]
    x_vals = [",".join([elem[0],str(elem[1])]) for elem in x_vals]
    plotly.offline.plot({
        "data":[Bar(x=x_vals,y=y_vals)],
        "layout":Layout(
            title="Frequency plot every day, every hour of backpage escort section"
        )
    },auto_open=False)
    shutil.move("temp-plot.html",filename)

def visualize_day_hour():
    time_freq = metric_generation.number_of_posts_in_adults_hour_over_hour()
    plot_simple_barchart(time_freq,"app/templates/backpage_day_hour.html")

def visualize_unique_day_hour():
    time_freq = metric_generation.unique_posts_per_hour_day_of_the_week()
    plot_simple_barchart(time_freq,"app/templates/unique_backpage_day_hour.html")
