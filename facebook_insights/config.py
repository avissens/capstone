import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/facebook_insights"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))
    
class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/facebook_insights-test"
    DEBUG = False
    SECRET_KEY = "Not secret"
    
class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "postgresql://localhost:5432/facebook_insights-test")
    DEBUG = False
    SECRET_KEY = "Not secret"
