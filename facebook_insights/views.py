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

from .database import User
from flask import flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/select')
@login_required
def select():
    return render_template('select.html')
    
@app.route('/login', methods=["POST"])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect username or password', 'danger')
        return redirect(url_for('login_get'))
    login_user(user)
    return redirect(request.args.get('next'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

#Supply args for URL
#page_name = "name"
#token = 'token'

#Calling API
@app.route('/chart', methods=['POST'])
@login_required
def ptat_post():
#Deleting the data for the next plot  
    session.query(FacebookInsights).delete()

#Convert dates
    date_since = request.form['since']
    date_until = request.form['until']
    date_since_format = datetime.datetime.strptime(date_since, '%d/%m/%Y')
    since = str(date_since_format.date())
    date_until_format = datetime.datetime.strptime(date_until, "%d/%m/%Y") + datetime.timedelta(days=1)
    until = str(date_until_format.date())

#Call Facebook API
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
            
#Querying the response            
    f_total = session.query(FacebookInsights.date, func.sum(FacebookInsights.value).label('total')).filter(FacebookInsights.gender=='F').group_by(FacebookInsights.date).all()
    m_total = session.query(FacebookInsights.date, func.sum(FacebookInsights.value).label('total')).filter(FacebookInsights.gender=='M').group_by(FacebookInsights.date).all()

#Manipulating dictionaries 
    ptat_dic_f = dict(f_total)
    ptat_dic_m = dict(m_total)
    peak_date = max(ptat_dic_f, key=ptat_dic_f.get)
    peak_day = peak_date.date()
    peak_date_dmy = datetime.datetime.strptime(str(peak_day), '%Y-%m-%d').strftime('%d/%m/%Y')
    peak_value = ptat_dic_f[peak_date]
    peak_value = format(peak_value, ',d')
    female_keys = list(ptat_dic_f.keys())
    female_values = list(ptat_dic_f.values())
    male_values = list(ptat_dic_m.values())

#Plotting results
    x = female_keys
    x = date2num(x)
    y = female_values
    z = male_values
    
    plt.figure(figsize=(10, 4.5))
    matplotlib.rcParams.update({'font.size': 10})
    ax = plt.subplot(111)
    width = 0.2
    opacity = 0.5
    ax.bar(x, y, width=width,color='orange',align='center', alpha=opacity)
    ax.bar(x+width, z, width=width,color='green',align='center', alpha=opacity)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    plt.xticks(x+(width/2), rotation=60)
    plt.title('People Talking About This by Gender')
    plt.ylabel('PTAT')
    plt.xlabel('Dates')
    plt.legend(['Female', 'Male'], loc='upper left')
    timestr = time.strftime("%Y%m%d-%H%M%S")
    plt.savefig('facebook_insights/static/charts/'+timestr+'.png')

#Getting all messages on the peak day
    peak_day_since = str(peak_day)
    peak_day_until = str(peak_day + datetime.timedelta(days=1))
    m = requests.get('https://graph.facebook.com/v2.8/'+page_name+'/posts?since='+peak_day_since+'&until='+peak_day_until+'&limit=100&access_token='+token+'')
    json_object_m = m.json()
    data_m = json_object_m['data']
    peak_picture = []
    peak_link = []
    peak_message = []
    peak_time = []
    posts = []
#Call Facebook API to get posts' data: picture, link, message
    for i in data_m:
        post_id = i['id']
        p = requests.get('https://graph.facebook.com/v2.8/'+post_id+'?fields=full_picture, picture, link, message, created_time&limit=100&access_token='+token+'')
#        print(p.status_code) #check that status of the response
        json_object_p = p.json()
        picture = json_object_p['full_picture'] #This is URL
        peak_picture.append(picture)
        posts_picture = peak_picture
        link = json_object_p['link'] #This is URL too
        peak_link.append(link)
        posts_link = peak_link
        message = json_object_p['message']
        peak_message.append(message)
        posts_message = peak_message
        timestamp = json_object_p['created_time']
        peak_time.append(timestamp[-13:-5])
        posts_time = peak_time
        posts = zip(posts_picture, posts_link, posts_message, posts_time)
        
    session.commit()
        
    return render_template('chart.html', page_name=page_name, timestr=timestr, since=date_since, until=date_until, peak_date=peak_date_dmy, peak_value=peak_value, data_m=data_m, posts=posts)