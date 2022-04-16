from flask import Blueprint

video = Blueprint("videos", __name__, url_prefix="/videos")

@video.route("/")
def base():
    return "this is the home"