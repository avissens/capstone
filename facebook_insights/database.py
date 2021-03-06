from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, Float, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from . import app

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/facebook_insights')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

#Create a user model
class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))

#Create Facebook API request model
class FacebookInsights(Base):
    __tablename__ = "facebook_insights"
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    gender = Column(String)
    age = Column(String)
    value = Column(Integer)
    
#dropping the table
#Base.metadata.drop_all(engine)
#creating the table
Base.metadata.create_all(engine)
session.query(FacebookInsights).delete()