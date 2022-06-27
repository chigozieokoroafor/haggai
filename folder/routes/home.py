from cmath import e
from email import message
from flask import Blueprint
from datetime import datetime

from flask import request
from bson import ObjectId 
from folder.database import daily_verse_db, devotion_list_db, mixlir_db, latest_db, sermon_db
from folder.functions import check_for_zero, check_date

import pymongo

from folder.routes.sermon import sermon

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
        #devotion_ = request.args.get("devotions")
        #devotion_list = devotion_.split(",")

        #------------------ for daily_verse  -------------------------------
        verse = daily_verse_db.find_one({"day": int(day),
                                                "year": int(year),
                                                "month": int(month) })
        if verse == None:
            verse_message = {}
        else:
            verse_message = verse

        #------------------ for audio,video, image  -------------------------------
        latest_video = latest_db.find({"type":"video"})
        latest_audio = latest_db.find({"type":"audio"})
        latest_image = latest_db.find({"type":"image"})
        

        latest_video_list = []
        latest_audio_list = []
        latest_image_list = []

        for video_item in latest_video:
            video_item.pop("_id")
            latest_video_list.append(video_item)
        
        for audio_item in latest_audio:
            audio_item.pop("_id")
            latest_audio_list.append(audio_item)

        for image_item in latest_image:
            image_item.pop("_id")
            latest_image_list.append(image_item)

        #------------------ for mixlir  -------------------------------

        mixlir = mixlir_db.find_one()
        
        if mixlir==None:
            mix = {}
        else:
            mixlir.pop("_id")
            mix = mixlir

        #------------------ for sermon_notes  ------------------------------
        sermons = sermon_db.find().sort([("timestamp",pymongo.DESCENDING)]).limit(5)
        sermon_list = []
        for sermon in sermons:
            sermon.pop("_id")
            sermon_list.append(sermon)


        #-------------------------for devotions--------------------------------------
        #for devotion_id in devotion_list:
        #    devotion = devotion_list_db.find_one({"_id":devotion_id})

        #-----------------------------------------------------------------
        data = {
            "daily_verse":verse_message,
            "latest_videos":latest_video_list,
            "latest_images":latest_image_list,
            "latest_audios":latest_audio_list,
            "sermons":sermon_list,
            "mixlir":mix
                }
        

        return data, 200