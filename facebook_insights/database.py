from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from . import app

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/facebook_insights')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

"""
from flask.ext.login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

#Create a user model (a generic user to be created later)
class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
"""

#Facebook API request model
class FacebookInsights(Base):
    __tablename__ = "facebook_insights"

    id = Column(Integer, primary_key=True)
    end_time = Column(DateTime, nullable=False)
    U1 = Column(Integer)
    U2 = Column(Integer)
    U3 = Column(Integer)
    U4 = Column(Integer)
    U5 = Column(Integer)
    U6 = Column(Integer)
    U7 = Column(Integer)
    F1 = Column(Integer)
    F2 = Column(Integer)
    F3 = Column(Integer)
    F4 = Column(Integer)
    F5 = Column(Integer)
    F6 = Column(Integer)
    F7 = Column(Integer)
    M1 = Column(Integer)
    M2 = Column(Integer)
    M3 = Column(Integer)
    M4 = Column(Integer)
    M5 = Column(Integer)
    M6 = Column(Integer)
    M7 = Column(Integer)
    
#creating a table
Base.metadata.create_all(engine)

"""
#creating a test instance
FacebookInsights1 = FacebookInsights(end_time = "2016-12-01T08:00:00+0000", U1 = 1, U2 = 2, U3 =3, U4 = 4, U5 = 5, U6 = 6, U7 = 7, F1 = 8, F2 = 9, F3 = 10, F4 = 11, F5 = 12, F6 = 13, F7 = 14, M1 = 15, M2 = 16, M3 = 17, M4 = 18, M5 = 19, M6 = 20, M7 = 21)
FacebookInsights2 = FacebookInsights(end_time = "2016-12-02T08:00:00+0000", U1 = 1, U2 = 1, U3 =2, U4 = 3, U5 = 4, U6 = 5, U7 = 6, F1 = 10, F2 = 10, F3 = 11, F4 = 20, F5 = 12, F6 = 1, F7 = 2, M1 = 1, M2 = 4, M3 = 7, M4 = 8, M5 = 9, M6 = 1, M7 = 1)
session.add_all([FacebookInsights1, FacebookInsights2])
session.commit()

#return the latest instance
latest_query = session.query(FacebookInsights.end_time).order_by(FacebookInsights.end_time.desc()).first()
print("Last query performed on: " + str(latest_query[0]))
#return the instance with the highest F1
F1_query, peak_date = session.query(FacebookInsights.F1, FacebookInsights.end_time).order_by(FacebookInsights.F1.desc()).first()
print("The highest number of F1 was " + str(F1_query) + " on " + str(peak_date))
"""