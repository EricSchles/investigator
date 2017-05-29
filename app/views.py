from app import app
from app import db
from flask import render_template, request, jsonify
from app.models import * #todo - import specific objects
from app.metric_generation import * #todo - import specific objects
from app.visualize_metrics import * #todo - import specific objects
from app.geographic_processing import contains
import json
from elasticsearch import Elasticsearch

#https://elasticsearch-py.readthedocs.io/en/master/
index_name = "image_search_index"

host = "http://localhost:9200"
es = Elasticsearch(host)

#how to do search courtesy of: https://marcobonzanini.com/2015/02/02/how-to-query-elasticsearch-with-python/
@app.route('/search', methods=['GET','POST'])
def search():
    query = request.form.get("query")
    print("got past query",query)
    results = es.search(index=index_name,body={"query":{"match": {"label":query}}})
    print("got to results")
    return render_template('results.html', results=results)

def to_dict(elem):
    dicter = elem.__dict__
    del dicter["_sa_instance_state"]
    dicter["timestamp"] = str(dicter["timestamp"])
    return dicter

def process_coordinate(elem):
    return elem.rstrip(")").lstrip("(").split("_")
    
@app.route("/api/coordinates/bounding_box/<query>")
def api_coordinates_bounding_box(query):
    box = [process_coordinate(elem) for elem in query.split(",")]
    lat_box = [elem[0] for elem in box]
    long_box = [elem[1] for elem in box]
    return jsonify({"query_result":[to_dict(elem) for elem in BackpageAdInfo.query.all() if contains(lat_box,long_box,(elem.latitude, elem.longitude))]})
    

@app.route("/api/phone_number/<query>")
def api_phone_number_query(query):
    return jsonify({"query_result":[to_dict(elem) for elem in BackpageAdInfo.query.filter_by(phone_number=query).all()]})

@app.route("/api/location/<query>")
def api_location_query(query):
    city,state = query.split(",")
    return jsonify({"query_result":[to_dict(elem) for elem in BackpageAdInfo.query.filter_by(state=state).all() if elem.city == city]})

@app.route("/api/coordinates/<query>")
def api_coordinates_query(query):
    latitude,longitude = query.split(",")
    return jsonify({"query_result":[to_dict(elem) for elem in BackpageAdInfo.query.filter_by(latitude=latitude).all() if elem.longitude == longitude]})

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

@app.route("/area_code_map",methods=["GET","POST"])
def area_code_map():
    locations = get_area_code_locations()
    locations = [to_geojson(location) for location in locations]
    return render_template("map_visual.html",locations=json.dumps(locations))
