from flask import Flask, render_template, request, redirect, url_for
from . import app
from .database import session, FacebookInsights
import datetime
import calendar
import requests
import re
from sqlalchemy import func
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num
import matplotlib.dates as mdates
import numpy as np
import operator

@app.route('/')
#@login_required
def index():
    return render_template('select.html')

#Supply args for URL    
#page_name = "name"
#token = 'token'

from .database import User
from flask import flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
"""
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))
"""

@app.route("/logout")
def logout():
    logout_user()
    return render_template("logout.html")

#Calling API
@app.route("/ptat", methods=["POST"])
#@login_required
def ptat_post():
#Convert ddMMMyyy into UNIX datestamp    
    date_since = request.form['since']
    date_until = request.form['until']
    date_since_unix = datetime.datetime.strptime(date_since, '%d/%m/%Y')
    since = str(int(date_since_unix.timestamp()))
    date_until_unix = datetime.datetime.strptime(date_until, "%d/%m/%Y")
    until = str(int(date_until_unix.timestamp()) + 86400)
    r = requests.get('https://graph.facebook.com/v2.8/'+page_name+'/insights/page_story_adds_by_age_gender_unique/day?since='+since+'&until='+until+'&access_token='+token+'')
    json_object = r.json()
    data = json_object['data']
    values = data[0]['values']
    gender_age_brackets = ('U.13-17','U.18-24','U.25-34','U.35-44','U.45-54','U.55-64','U.65+','F.13-17','F.18-24','F.25-34','F.35-44','F.45-54','F.55-64','F.65+','M.13-17','M.18-24','M.25-34','M.35-44','M.45-54','M.55-64','M.65+')
    ptat_dic = dict.fromkeys(gender_age_brackets)
#Iterate through the response
    values = data[0]['values']
    for item in values:
        date = item['end_time']
        for key in gender_age_brackets:
            ufm = item['value'].get(key, 0)
            ptat_dic[key] = ufm
            ptat = FacebookInsights(date=date, gender=key[0], age=key[2:], value=ufm)
            session.add(ptat)
            session.commit()

#Querying the response            
    f_total = session.query(FacebookInsights.date, func.sum(FacebookInsights.value).label('total')).filter(FacebookInsights.gender=='F').group_by(FacebookInsights.date).all()
    m_total = session.query(FacebookInsights.date, func.sum(FacebookInsights.value).label('total')).filter(FacebookInsights.gender=='M').group_by(FacebookInsights.date).all()
    print(f_total)
#Manipulating dictionaries
    ptat_dic_f = dict(f_total)
    ptat_dic_m = dict(m_total)
    peak_date = max(ptat_dic_f, key=ptat_dic_f.get)
    peak_day = peak_date.date()
    peak_value = ptat_dic_f[peak_date]
    peak_value = format(peak_value, ",d")
    female_keys = list(ptat_dic_f.keys())
    female_values = list(ptat_dic_f.values())
    male_values = list(ptat_dic_m.values())

#Plotting results
    x = female_keys
    x = date2num(x)
    y = female_values
    z = male_values
    
    width=0.2
    ax = plt.subplot(111)
    opacity = 0.7
    ax.bar(x, y, width=0.2,color='r',align='center', alpha=opacity)
    ax.bar(x+width, z, width=0.2,color='b',align='center', alpha=opacity)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    plt.xticks(x+(width/2), rotation=70)
    plt.title('People Talking About This by Gender')
    plt.ylabel('PTAT')
    plt.xlabel('Dates')
    plt.legend(['Female', 'Male'], loc='upper left')
    timestr = time.strftime("%Y%m%d-%H%M%S")
    plt.savefig('facebook_insights/static/charts/'+timestr+'.png')
    return render_template("chart.html", timestr=timestr, since=date_since, until=date_until, peak_date=peak_day, peak_value=peak_value, page_name=page_name)

#printing lots of stuff for testing    
#    print(session.query(FacebookInsights.date).distinct().all())
#    print(session.query(FacebookInsights.gender).distinct().all())
#    print(session.query(FacebookInsights.age).distinct().all())
#    print(session.query(FacebookInsights.date).order_by(FacebookInsights.date.desc()).first())
#    print(session.query(FacebookInsights.value).order_by(FacebookInsights.value.desc()).first())
#    f_query, f_peak_date = session.query(FacebookInsights.value, FacebookInsights.date).filter(FacebookInsights.gender=='F').order_by(FacebookInsights.value.desc()).first()
#    print("The highest number of female users was " + str(f_query) + " on " + str(f_peak_date))


    
