from email import message
from flask import Blueprint
from datetime import datetime

from flask import request
from bson import ObjectId 
from folder.database import daily_verse_db, devotion_list_db, mixlir_db, audio_db, image_db, live_videos_db, videos_db, latest_db
from folder.functions import check_for_zero, check_date

import pymongo

# create extra endpoints for the daily verses to ad

#call all the home features in one endpoint
home = Blueprint("home", __name__, url_prefix="/api/haggai/home")

date = datetime.utcnow()
date_ = date.strftime("%Y-%m-%d %H:%M:%S" ) 

@home.route("/")
def base():
    return "this is the home"


#this endpoint is for getting all items 
@home.route("/all", methods=["GET"])
def all_items():
    
    if request.method == "GET":
        day = request.args.get("day")
        month = request.args.get("month")
        year = request.args.get("year")
        verse = daily_verse_db.find_one({"day": str(check_for_zero(day)),
                                                "year": str(year),
                                                "month": str(check_for_zero(month))})
        if verse == None:
            verse_message = {}
        else:
            verse_message = verse


        latest_video = latest_db.find({"type":"video"})
        latest_audio = latest_db.find({"type":"audio"})
        latest_image = latest_db.find({"type":"image"})
        

        latest_video_list = []
        latest_audio_list = []
        latest_image_list = []

        for video_item in latest_video:
            
            latest_video_list.append(video_item)
        
        for audio_item in latest_audio:
            
            latest_audio_list.append(audio_item)
        
        for image_item in latest_image:
            
            latest_image_list.append(image_item)


        mixlir = mixlir_db.find_one()
        if mixlir==None:
            mix = {}
        else:
            mix = mixlir

        data = {
            "daily_verse":verse_message,
            "latest_videos":latest_video_list,
            "latest_images":latest_image_list,
            "latest_audios":latest_audio_list,
            
        }
        data["mixlir"] = mix

        return data, 200