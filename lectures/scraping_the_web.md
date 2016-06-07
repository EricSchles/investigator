#Scraping the Web

##Background and setup - I'm going to 'install' some ideas in you.

Scraping the web for data is about mapping one representation into another, often a database.  With this transformation of information into a local context, certain information maybe lost, or abstracted.  Thusly, the idea of scraping the web can be hard, but doing the actual scraping is usually straight forward.  

The important thing to understand is not the mapping of context from one technical medium - the web, to another - a database.  But instead the ideological mapping, from a dynamic context to a static one.  For this we need metadata about our web information and semantic information about the domain we are scraping.  This will allow us the ability to compress unnecessary information, infer missing data from backend processes we can't see, and make sense of the unstructured semantics of the web.

What this translates to?  Taking information from one database and sending it to another, via a Rube Goldberg machine of tools and techniques.

##A Trivial Example

Getting started with web scraping is pretty straight forward.  However the skill level needed to do web scraping right goes from simple to intermediate to advanced.  We'll try to treat each of the necessary pieces in kind, moving through different types of concerns section by section.  By the end of this document, you should be an expert in scraping any kind of web site, for any reason.

So, let's scrape something!

From the command line run:

`pip install requests`

if you don't have pip you can get [pip here](https://pip.pypa.io/en/stable/installing/)

```
r = requests.get("https://www.google.com")
print(r.url)
print(r.text)
```

We can treat `requests.get([website])` as the same thing as pointing your browser to `[website]`.  The returned objected, abbreviated as `r`, stands for response.  As in the response from one of google's servers to the `get` request issued by `requests`.


##How do I even?

The first thing to note, if you ran the above commands (either via a python shell or saving things to a script), is that you just get back a string.  So how do you pull out meaningful information from this?

There are a number of great tools for scraping the web, but my personal favorite is lxml.  To get lxml you may have to do a little work, but it's worth it (and then some!).  

[lxml's documentation](http://lxml.de/installation.html) recommends doing the following:

`STATIC_DEPS=true sudo pip install lxml`

Which might be wrong, depending on your build - the key is you'll need `libxml2` and `libxslt`, which don't come with mac.  When I was running into this problem I used brew to install `libxml2` and `libxslt`:

`brew install libxml2 libxslt`

As an alternative, you could always get an linux vm (I recommend ubuntu) and install everything there.  Sadly, that's out of scope for this tutorial, but I'm happy to do another one on installing vm's and post it here.  

So, why did I ask you to go through all that effort?

```
import requests
import lxml.html

r = requests.get("https://www.google.com")
html = lxml.html.fromstring(r.text)
print(html.xpath("//a/@href"))
```

`lxml` exposes a parser for html pages that is superb.  The parser can be used a lot of ways, but I'd say the canonical way is to make use of the `xpath` api exposed through the library.  If you're unfamiliar with xpath, you can kind of think it like regular expressions for parsing web pages.  We'll make deep use of it throughout this tutorial, so it's recommended that you find a reference or two.

* [w3 schools](http://www.w3schools.com/xsl/xpath_intro.asp) has a good tutorial on this.  

* [Some advanced examples](https://renderman.pixar.com/resources/current/RenderMan/xPathExamples.html).

Let's start with understanding how xpath treats a document and then we'll move into the specifics of the above xpath query.  

lxml treats html documents as Directed Acyclic Graph's, typically referred to as trees.  The root of the document is the highest level - the openning and closing `<html>`,`</html>` tags.  Each layer of tree is one level deeper in the tag hierarchy so, in the following html:

```
<html>
<head>
	<title></title>
</head>
<body>
	<p>Hello</p>
</body>
</html>
```

The second layer is the head tag and the body tag.  At the third layer is the title tag and the p tag.  As should be clear from the example - the layer of your tag is determined by how many other tags enclose it.  The more tags enclose the tag your interested in, the deep in the tree it exists.

Let's break down the above xpath "query".

`//[tag]` - says search the whole document, at every layer for this [tag] type.  In our case - `//a` will return all the a tags.  

`/@[attribute]` - The `@` symbol is used to denote a tag attribute - and specifically return everything of this type.  Assuming the attribute is defined for the tag - in this case `//a/@href` returns the hyper link for the a tag.

What happens when we want other attributes or data?  

In the case of wanting other attributes we can make use of a whole host of methods to get the relevant metadata (aka the values of certain attributes) or we can get the text used for the hyper links via the following:

```
import requests
import lxml.html

r = requests.get("https://www.google.com")
html = lxml.html.fromstring(r.text)
print("Names of links:")
print([elem.text_content() for elem in html.xpath("//a")])
print("Links themselves:")
print(html.xpath("//a/@href"))
```

All done ;)

#Understanding What We Are Scraping

Now that we have some notion of how to scrape data from the internet, I'm going to bring in some background into what we'll be scraping.  In this case we'll be scraping backpage - looking instances of human trafficking.  Understanding that the data is out there, is not enough to bring people to justice for the things they've done, but it's a start.

The truth is we are investigating a set of complex actors that work, often times together in complex ways.  Capturing this complexity can be a challenge.  But it's best to start with the market place.  By understanding how to get information from backpage, we can abstract out to the pocket websites which capture information about sex slavery.  To put a more economic context to our understanding - backpage can be thought of as the supply side of sex slavery whereas, understanding the buyers, informs the demand side.  At present little formal work has been to understand these market places.  People tend to focus on specific cases or investigations, rather than understanding the markets as a whole.  

The ultimate goal of what we are trying to do here is complex - to understand the forces that contribute to changes in the supply and demand of sex slavery.  And if possible, to manipulate the market into contracting.  To do this, we need a set of effective data driven policy levers.  By understanding the scraped data, we have insight into just that.  At the very least, by fully understanding the market place for sex slavery, we force the actors to "go underground" to the deep web.  While some people will follow, it is possible many of the less technically sophisticated actors won't.  In which case, just by inspecting the market, we shrink it.  The best case scenario, is no deep web retreat happens, and traffickers continue to act in the open.  In this case, we can leverage their data to make real policy decisions, to systematically shrink the market, in a dynamic, reactive way.  

##Breaking down backpage intro metrics

![](pictures/craigslist.png)

The above picture is taken from craigslist, but the visual is better and more or less equivalent for backpage.  Second hand market places for goods and services have become ubiquitious across every community in the united states.  In fact, we can treat craigslist as a proxy for every community - the more people - the more craigslist's there will be.  This is because craigslist is not local - it exists for every community.  It is a digital representation of all our "informal" commerce.  Backpage operates very much the same way - except they have a much larger footprint in the sex slavery space and a somewhat smaller footprint in all other spaces.  

###Our first metric

Understanding how to relate craigslist and backpage in this context is our first web scraping task.  We can use craigslist to get a sense of the full market size for a given community.  Where a full community is modeled as a craigslist for an area.  And then we can treat the market segment interested in the purchase and sale of sex as those represented on backpage.  Thus we can get an accurate sense of market size and a metric I will call relative willingness to purchase sex commercially.  It's important to note - not all commercial sex is sex slavery, but all sex slavery is commercial sex.  So how do we get to a precise answer of how much is going on?  Using only data from the web, we don't.  Instead, we will write our tools from the context of an investigator working in a district attorney's office or police department.  Thus, we never know how bad or terrible the sex trafficking happening is, with precision.  However, we will still have an upper bound and isn't that all computer scientists care about anyway ;)  For clarity, the joke here is comparing measuring the size of sex trafficking to big Oh-notation, I am not claiming computer scientists don't care.  (They care a lot!)

Investigators have the opposite problem, as compared to the civicly minded developer - all the data and none of the resources.  By creating tools for such an investigator, we can implicitly aid in the search for human traffickers.  But more over, by understanding how to build for investigators, we don't run the legal, or personal risk of investigating dangerous criminals.  

So to recap - our first metric comes from taking the proportion of web traffic from craigslist and backpage's adult section and comparing the two.  The resulting proportion will tell us the market segment interested in purchasing sex.  And we will define it as relative willingness to purchase commercial sex.

###Our second type of metrics

Now that we have a good idea of how much of the relative population is interested in purchasing commercial sex, let's get a better sense of that population in detail.  There will be two metrics here:

1.  The overall number of posts in the adults section, month over month.
2.  The average rate at which ads are posted on backpage's adult section per hour.

We will measure this second metric every hour, creating a canonical hour per hour.  So we will have a standard rate of posting for 9 am, on tuesdays; for 10am on tuesdays, and so on.  Eventually, we'll get to a set of distributions - one for every hour of every day of the week.  The overall number of posts per month, get's us to larger seaonality affects.  Whereas the hour by hour, gives a sense of how things change within normal scale. 

###Our third type of metric

Now that we have a sense of the national level, a sense of the local level, we are ready to start thinking about other types of measurement.  There is a lot of discussion around hard metrics - data that cannot be faked and that matters for investigators.  For this we will use phone numbers, and locations.  These pieces of information don't just tell us something important in general like,

* an upper bound on the number of unique posters per day,
* an upper bound on the number of unique posters per day per hour,
* the number of unique phone numbers posted per day
* the frequency of use, by location

They can also be used directly by investigators to link a case to a set of ads.  We care about this, because most human trafficking cases come into an investigator as domestic violence and then it is on the investigator to prove the link to human trafficking.  At this point a formal legal definition makes sense:

Sex slavery is domestic violence, being deprived of money, and being sold for commercial sex.  

While domestic violence isn't a necessary condition from a legal context, it is always happening, otherwise you can't force the victim to stay a victim.  And thuse traffickers use violence to force victims to engage in commercial sex.  There are very few rules in life.  But the sad truth is, this is one of them.

###Tying in outside data

It's worth noting at this point, that we can take the location data and tie it together with lots and lots of other data sets, like:

* education data
* income data
* ethnographic information
* demographic information
* general crime data
* policy data
* legal data
* and more!

Tying in these other data sets will give us a clearer picture of the types of residents and give us a broader sense of the types of individuals existing in the community.  From there we can understand the set of conditions, leading to rises or falls in the market for commercial sex.  With aid from police departments, we can extend this to understanding the rise and fall of human trafficking.  And then, with a data driven approach, we can apply our policy levers to reduce the markets in size and scale.

#Bringing ideas and technology together

Now that we've established the conceptual framework for what we are going to measure, we are in a place to begin attacking the problem.  For this, I'll be showing you how to scrape backpage.  It's worth noting website like backpage are adversial in nature, they don't want you to scrape their data.  So extra challenges will occur that will lead us down some technically challenging paths.

##Plan

We'll build up the terms and tools methodically for scaping.

* Pick a place to scrape on backpage - backpage is ordered by city and state and there are backpage websites for each location (much like lots of the federal government).  

* Pick a subset of the adult content to scrape

* Start scraping

* decide what to store and how to store it

* set up our database

* do exploratory data analysis around our data

* create data visualizations of our findings

* do prediction and model selection to understand our data in detail

* do probabilistic analysis to understand our underlying distributions and how different random variables inter relate

* generalize out our scraper to work over all of backpage

* start scaling out our data concerns to allow 

* bring in other data sources

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


