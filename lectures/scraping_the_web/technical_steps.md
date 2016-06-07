
##Picking a place

Because I'm in new york city, we'll focus our efforts on this, so we'll use:

`http://newyork.backpage.com/`

As our base url and we'll choose the escorts category as the place we'll scrape.

`http://newyork.backpage.com/FemaleEscorts/`

##Start scraping

The first thing we need to do, is be able to scrape the first page, on a time lapse for all of it's links relating to advertisements for sex.

![](pictures/backpage_ads_list.png)

We'll use the chrome browsers inspect utility to understand the structure of the ads.

![](pictures/inspect_element.png)

All the ads we are interested in are of the form:

![](pictures/ad_url.png)

In order to do this, we need one of the built in methods that comes with xpath: contains

`//div[contains(@class,'cat')]/a/@href"`

Notice that the number next to cat changes from ad to ad, but cat is a textual invariant.  Therefore we simply need to make sure the tag contains the class cat.

So how does this work:

```
import requests
import lxml.html
import time
import random

while True:
	r = requests.get("http://newyork.backpage.com/FemaleEscorts/")
	html = lxml.html.fromstring(r.text)
	ads = html.xpath("//div[contains(@class,'cat')]/a/@href")
	time.sleep(random.randint(2,700)) #sleep for 6 minutes
```

##Deciding on what to store and how to store it

Now that we have all the links on a page we are actually ready to start figuring out metrics of type 2!  So let's store the frequency of pages scraped per hour:

```
import requests
import lxml.html
import time
from datetime import datetime
import random

time_frequency = []
while True:
	r = requests.get("http://newyork.backpage.com/FemaleEscorts/")
	html = lxml.html.fromstring(r.text)
	ads = html.xpath("//div[contains(@class, 'cat')]/a/@href")
	time_frequency.append((datetime.now(),len(ads))
	time.sleep(random.randint(2,700))
```

##Setup our database

For our application we'll be making use of Flask and SQLAlchemy.  For this we'll need the Flask and Flask-SQLAlchemy packages:

```
pip install flask
pip install flask-sqlalchemy

```

Here's the directory structure for our application:

```
investigator/
	run_scraper.py
	app/
		__init__.py
		views.py
		scrapers.py
		models.py
```

We will use Postgres to store our records.

Installing postgres:

Mac: `brew install postgres`

Or

Linux: `sudo apt-get install postgres`

How to postgres (from the command line):

* Listing all the users: `psql -l`
* Create user: `createuser -P -s -e -d username`
* Create DB: `createdb [database_name]`
* running postgresql: `psql [database_name]`
* delete DB: `dropdb [database_name]`

So we are going to create a user:

`createuser -P -s -e -d eric_s`

Create a database:

`create backpage_ads -U eric_s`

__init__.py:

```
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

username,password = "eric_s","1234"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://"+username+":"+password+"@localhost/backpage_ads"
db = SQLAlchemy(app)

from app import views,models
```

models.py:

```
from app import db

class Backpage(db.Model):
	__tablename__ = 'backpage'
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime)
	frequency = db.Columb(db.Integer)

	def __init__(self,timestamp,frequency):
		self.timestamp = timestamp
		self.frequency = frequency
```

views.py:

```
from app import app
```

Notice that we leave views.py more or less unimplemented at the moment.  This is because our process will need to run continuously unless explicitly stopped, either by the system administrator or by some other condition.  For this, we'll need to build up an admin panel, which will take us slightly far afield from our current goal of just setting a database :)

scrapers.py:

```
import requests
import lxml.html
import time
from app import db
from app.models import Backpage
from datetime import datetime
import random

def scrape_backpage():
	while True:
		r = requests.get("http://newyork.backpage.com/FemaleEscorts/")
		html = lxml.html.fromstring(r.text)
		ads = html.xpath("//div[contains(@class, 'cat')]/a/@href")
		bp = Backpage(datetime.now(),len(ads))
		db.session.add(bp)
		db.session.commit()
		time.sleep(random.randint(2,700))
```

run_scrapers.py:

```
from app import scrapers

scrapers.scrape_backpage()
```

##Visualizing our Data

Now that we have some minimal infrastructure in place, and somewhere to store our data we are ready to start really building out our metrics, visualizing them, analyzing them.

We will be automating our analysis across a few directions - visually and via text generated reports.  

For this we'll first need to take our raw data and turn it into a real timeseries.  We'll do this at the hour by hour cross section and month over month.  

```
from app.models import Backpage
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
            day_hours[(day,hour)] += day_hours[(day,hour)] + (1/ind*(frequencies[ind] - day_hours[(day,hour)])
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

def overall_number_of_posts_in_adults_month_over_month():
    list_of_ads = Backpage.query.all()
    datetimes = [elem.timestamp for elem in list_of_ads]
    frequencies = [elem.frequency for elem in list_of_ads]
    month_over_month_frequencies = prepare_for_month_over_month_timeseries(datetimes,frequencies)
    return month_over_month_frequencies
```

Let's see what our two "public" functions return:

```
from app import metric_generation
>>> metric_generation.overall_number_of_posts_in_adults_month_over_month()
([datetime.datetime(2016, 6, 7, 0, 0)], [300])
>>> metric_generation.number_of_posts_in_adults_hour_over_hour()
{('Tuesday', 11): 300}
```

This suggests:
 
 * timeseries for `overall_number_of_posts_in_adults_month_over_month` and
 * a bar graph for `number_of_posts_in_adults_hour_over_hour`

Visually representing this data:

In order to visually represent our data, we'll make use of [plotly](https://plot.ly/).

visualize_metrics.py:

```
from app import metric_generation
import shutil
from collections import OrderedDict
import plotly
from plotly.graph_objs import Bar,Layout,Scatter, Box, Annotation,Marker,Font,XAxis,YAxis
from datetime import datetime
import shutil

def plot_simple_timeseries(dates,frequencies,filename):
    x_vals = dates
    y_vals = frequencies
        
    plotly.offline.plot({
        "data":[Scatter(x=x_vals,y=y_vals)],
        "layout":Layout(
            title="Time Series analysis of backpage escort section"
        )
    })
    shutil.move("temp-plot.html",filename)

def visualize_month_over_month():
    months,frequencies = metric_generation.overall_number_of_posts_in_adults_month_over_month()
    plot_simple_timeseries(months,frequencies,"app/templates/backpage_month_over_month_frequencies.html")

visualize_month_over_month()
```

Generates:

![](pictures/bar_chart.png)

And

```
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
    })
    shutil.move("temp-plot.html",filename)

def visualize_day_hour():
    time_freq = metric_generation.number_of_posts_in_adults_hour_over_hour()
    plot_simple_barchart(time_freq,"app/templates/backpage_day_hour.html")
```

Generates:

![](pictures/line_chart.png)

As you can see from the two above charts (with semi-faked data) plotly creates visually pleasing charts, easily.  The real challenge comes from pre-processing the data, which is an acceptable tradeoff.


