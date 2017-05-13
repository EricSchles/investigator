from app import app
from app import db
from flask import render_template, request, jsonify
from app.models import * #todo - import specific objects
from app.metric_generation import * #todo - import specific objects
from app.visualize_metrics import * #todo - import specific objects
import json

@app.route("/api/phone_number/all")
def api_phone_number_all():
    return jsonify({"all_phone_numbers":[elem.phone_number for elem in BackpageAdInfo.query.all()]})

@app.route("/api/coordinates/all")
def api_coordinates_all():
    return jsonify({"all_coordinates":[(elem.latitude,elem.longitude) for elem in BackpageAdInfo.query.all()]})

@app.route("/api/location/all")
def api_location_all():
    return jsonify({"all_locations":[(elem.city,elem.state) for elem in BackpageAdInfo.query.all()]})

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/posts_hourly",methods=["GET"])
def number_of_posts_in_adults_hour_over_hour():
    visualize_day_hour()
    return render_template("backpage_day_hour.html")

@app.route("/area_code_analysis",methods=["GET"])
def area_code_analysis():
    phone_numbers = [elem.phone_number for elem in BackpageAdInfo.query.all()]
    area_codes = {}
    for number in phone_numbers:
        area_code = number[:3]
        if "{" in area_code:
            area_code = number[1:4]
        if area_code not in list(area_codes.keys()):
            area_codes[area_code] = 1
        else:
            area_codes[area_code] += 1
    return render_template("area_code_analysis.html",area_codes=area_codes)

@app.route("/list_phone_numbers",methods=["GET"])
def list_phone_numbers():
    phone_numbers = list(set([elem.phone_number for elem in BackpageAdInfo.query.all()]))
    numbers = {}
    for phone_number in phone_numbers:
        numbers[phone_number] = len(BackpageAdInfo.query.filter_by(phone_number=phone_number).all())
    return render_template("list_phone_numbers.html",phone_numbers=numbers)

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
