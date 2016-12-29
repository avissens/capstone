import os
from facebook_insights import app
from flask import Flask, render_template, request
from facebook_insights.database import session, FacebookInsights, User
import datetime
import calendar
import requests
import re
from getpass import getpass
from werkzeug.security import generate_password_hash
from flask_script import Manager
manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

@manager.command
def adduser():
    username = input("Username: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return

    password = ""
    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(username=username, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()

#Remove any files in facebook_insights/charts/ older than 7 days
'''
import os, sys, time
from subprocess import call

now = time.time()
cutoff = now - (7 * 86400)

charts = os.listdir("facebook_insights/charts")
for chart in charts:
    if not chart.endswith(".png"): 
        continue
    if os.path.isfile( "facebook_insights/charts/" + chart ):
            t = os.stat( "facebook_insights/charts/" + chart )
            c = t.st_ctime

            # delete file if older than a week
            if c < cutoff:
                    os.remove("facebook_insights/charts/" + chart)
'''

if __name__ == "__main__":
    manager.run()