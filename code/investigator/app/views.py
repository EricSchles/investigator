from app import app
from app import db
from flask import render_template,request
from app.models import *
from app.metric_generation import *
from app.visualize_metrics import *

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/unique_posts_hourly",methods=["GET"])
def number_of_posts_in_adults_hour_over_hour():
    visualize_day_hour()
    return render_template("backpage_day_hour.html")

@app.route("/posts_monthly",methods=["GET"])
def overall_number_of_posts_in_adults_month_over_month():
    visualize_month_over_month()
    return render_template("backpage_month_over_month_frequencies.html")


