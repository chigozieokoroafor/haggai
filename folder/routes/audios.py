from flask import Blueprint, request
from folder.database import audio_db

audios = Blueprint("audios", __name__, url_prefix="/audios")

@audios.route("/")
def base():
    return "this is the home"

@audios.route("/audio/<first_id>/<second_id>/<third_id>/<fourth_id>/<fifth_id>", methods=["POST", "GET"])
def audio(first_id, second_id=None, third_id=None,fourth_id=None,fifth_id=None):
    if request.method == "POST":
        info = request.json
        audio_url = info.get("audio_url")
        audio_name = info.get("audio_name")
        doc_id = info.get("id")
        if first_id :
            nav = audio_db.find_one({"id":first_id})
            if nav["final"] == True:
                audio_db.insert_one({"audio_url":audio_url,
                             "audio_name":audio_name,
                             "rank":int(str(audio_db.count_documents({}))+"0" )  +10,
                             "parent_folder":first_id
                             })
        return {"message":"audio data updated"}, 200
    if request.method == "GET":
        info = request.json
        parent_folder = info.get("parent_folder")
        audio_= []
        audio = audio_db.find({"parent_folder":parent_folder})
        for item in audio:
            d = {}
            d["audio_name"] = item["audio_name"]
            d["audio_url"] = item["audio_url"]
            d["rank"] = item["rank"]
            d["parent_folder"] = item["parent_folder"]
            audio_.append(d)
        return {"items":audio_}

