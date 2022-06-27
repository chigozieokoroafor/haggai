from flask import Flask
from flask_cors import CORS
from datetime import datetime
from folder.routes.audios import audios
from folder.routes.themes import theme
from folder.routes.devotions import devotions
from folder.routes.home import home 
from folder.routes.videos import video
from folder.routes.images import image
from .routes.devotion_types import devotion_types_bp
from folder.routes.mixlir import mixlir
from folder.routes.daily_verse import verse
from folder.routes.sermon import sermons

    



app  = Flask(__name__)
CORS(app)



app.register_blueprint(blueprint=audios,name="audios")
app.register_blueprint(blueprint=theme,name="themes")
app.register_blueprint(blueprint=devotions, name="devotions")
app.register_blueprint(blueprint=home, name="home")
app.register_blueprint(blueprint=video, name="videos")
app.register_blueprint(blueprint=image, name="images")
app.register_blueprint(devotion_types_bp, url_prefix='/devotion_types')
app.register_blueprint(blueprint=mixlir, name="mixlir")
app.register_blueprint(blueprint=verse, name="daily_verse")
app.register_blueprint(blueprint=sermons, name="sermons")