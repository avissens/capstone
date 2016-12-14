#import os
from flask import Flask, render_template, request
from . import app
from .database import session, FacebookInsights
import datetime
import calendar
import requests


@app.route('/')
def index():
    return render_template('index.html')
    
from flask import request, redirect, url_for

#from flask.ext.login import login_required
#from flask import flash
#from flask.ext.login import login_user, logout_user
#from werkzeug.security import check_password_hash
#from .database import User
#from werkzeug.security import generate_password_hash

#Storing API response
@app.route("/ptat", methods=["POST"])
#@login_required
def ptat_post():
#Convert ddMMMyyy into UNIX datestamp    
    date_since = request.form['since']
    date_until = request.form['until']
    date_since_unix = datetime.datetime.strptime(date_since, "%d%b%Y")
    since = str(calendar.timegm(date_since_unix.utctimetuple()))
    date_unitl_unix = datetime.datetime.strptime(date_until, "%d%b%Y")
    until = str(calendar.timegm(date_unitl_unix.utctimetuple()))
#Supply args for URL    
    page_name = 'page_name'
    token = 'token'
    r = requests.get('https://graph.facebook.com/v2.8/'+page_name+'/insights/page_story_adds_by_age_gender_unique/day?since='+since+'&until='+until+'&access_token='+token+'')
    json_object = r.json()
    data = json_object['data']
    values = data[0]['values']
    gender_age_brackets = ('U.13-17','U.18-24','U.25-34','U.35-44','U.45-54','U.55-64','U.65+','F.13-17','F.18-24','F.25-34','F.35-44','F.45-54','F.55-64','F.65+','M.13-17','M.18-24','M.25-34','M.35-44','M.45-54','M.55-64','M.65+')
    ptat_dic = dict.fromkeys(gender_age_brackets)
    #Iterate through the response
    values = data[0]['values']
    for item in values:
      end_time = item['end_time']
      for v in item['value']:
        ptat_list = []
        for key in gender_age_brackets:
          ufm = item['value'].get(key, 0)
          ptat_dic[key] = ufm
          ptat_list.append(ufm)
        ptat = FacebookInsights(
            end_time = end_time,
            U1 = ptat_list[0],
            U2 = ptat_list[1],
            U3 = ptat_list[2],
            U4 = ptat_list[3],
            U5 = ptat_list[4],
            U6 = ptat_list[5],
            U7 = ptat_list[6],
            F1 = ptat_list[7],
            F2 = ptat_list[8],
            F3 = ptat_list[9],
            F4 = ptat_list[10],
            F5 = ptat_list[11],
            F6 = ptat_list[12],
            F7 = ptat_list[13],
            M1 = ptat_list[14],
            M2 = ptat_list[15],
            M3 = ptat_list[16],
            M4 = ptat_list[17],
            M5 = ptat_list[18],
            M6 = ptat_list[19],
            M7 = ptat_list[20],
        )
    session.add(ptat)
    session.commit()
    print(session.query(FacebookInsights.end_time).all())
    return render_template('ptat.html')
