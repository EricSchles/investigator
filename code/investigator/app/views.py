from app import app
from app import db
from flask import render_template,request
from app.models import *
from app.metric_generation import *
from app.visualize_metrics import *
import json

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/posts_hourly",methods=["GET"])
def number_of_posts_in_adults_hour_over_hour():
    visualize_day_hour()
    return render_template("backpage_day_hour.html")

@app.route("/posts_monthly",methods=["GET"])
def overall_number_of_posts_in_adults_month_over_month():
    visualize_month_over_month()
    return render_template("backpage_month_over_month_frequencies.html")

@app.route("/unique_posts_hourly",methods=["GET"])
def number_of_unique_posts_in_adults_hour_over_hour():
    visualize_unique_day_hour()
    return render_template("unique_backpage_day_hour.html")

@app.route("/unique_posts_monthly",methods=["GET"])
def overall_number_of_unique_posts_in_adults_month_over_month():
    visualize_unique_month_over_month()
    return render_template("unique_backpage_month_over_month_frequencies.html")

def to_geojson(coordinates):
    dicter = {}
    dicter["type"] = "Feature"
    dicter["properties"] = {}
    dicter["geometry"] = {
        "type":"Point",
        "coordinates":[float(coordinates[0]), float(coordinates[1])]
        }
    return dicter

@app.route("/map_visual",methods=["GET","POST"])
def map_visual():
    locations = get_locations()
    locations = [to_geojson(location) for location in locations]
    return render_template("map_visual.html",locations=json.dumps(locations))
