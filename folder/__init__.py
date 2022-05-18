from email.mime import audio
from flask import Flask, request 
from flask_cors import CORS
from datetime import datetime
from folder.routes.audios import audios #, themes, devotions, home, videos, images
from folder.routes.themes import theme
from folder.routes.devotions import devotions
from folder.routes.home import home 
from folder.routes.videos import video
from folder.routes.images import image
#import json
#from requests import Request, Session
#from flask_apscheduler import APScheduler
    

from folder.functions import getToday



app  = Flask(__name__)
CORS(app)



app.register_blueprint(blueprint=audios,name="audios")
app.register_blueprint(blueprint=theme,name="themes")
app.register_blueprint(blueprint=devotions, name="devotions")
app.register_blueprint(blueprint=home, name="home")
app.register_blueprint(blueprint=video, name="videos")
app.register_blueprint(blueprint=image, name="images")

