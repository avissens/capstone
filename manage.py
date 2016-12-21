import os
from facebook_insights import app
from flask import Flask, render_template, request
from facebook_insights.database import session, FacebookInsights
import datetime
import calendar
import requests
import re

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

'''
from getpass import getpass
from werkzeug.security import generate_password_hash
from facebook_insights.database import User

def adduser():
    name = input("Name: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return

    password = ""
    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()
'''
'''
@app.route("/ptat", methods=["POST"])
#@login_required
#API request
def ptat_request():
#Convert ddMMMyyy into UNIX datestamp    
    date_since = request.form['since']
    date_until = request.form['until']
    date_since_unix = datetime.datetime.strptime(date_since, "%d%b%Y")
    since = str(calendar.timegm(date_since_unix.utctimetuple()))
    date_unitl_unix = datetime.datetime.strptime(date_until, "%d%b%Y")
    until = str(calendar.timegm(date_unitl_unix.utctimetuple()))
#Supply args for URL    
    page_name = 'NAME'
    token = 'TOKEN'
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
    return render_template("chart.html")
'''

if __name__ == '__main__':
    run()