from flask import Flask, request 
from flask_cors import CORS
from datetime import datetime 
from .devotion_types.devotion_types import devotion_types_bp
from .devotions.devotions import devotions_bp 

def check_for_zero(x):
    num = []
    x = int(x)
    if x<10:
        for i in str(x):
            number = int(i)
            num.append(number)
        if num[0]!=0:return '0'+ str(x)
        else: return x       
    else: return x

def check_date(datetime_):
    today = datetime.utcnow().date()
    d_ = datetime.strptime(datetime_, "%Y-%m-%d %H:%M:%S")
    date = d_.date()
    check = today > date
    return check

def check_live():
    date_.date


date = datetime.utcnow()
date_ = date.strftime("%Y-%m-%d %H:%M:%S" ) 


app  = Flask(__name__)
CORS(app)

app.register_blueprint(devotion_types_bp, url_prefix='/devotion_types')
app.register_blueprint(devotions_bp, url_prefix='/devotions')
from folder import routes

