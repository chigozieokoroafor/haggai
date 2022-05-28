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
        verse = daily_verse_db.find_one({"day": str(check_for_zero(date.day)),
                                                "year": str(date.year),
                                                "month": str(check_for_zero(date.month))})            
        verse_message = {"verse":verse}


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
            "live_videos":latest_video_list,
            "latest_images":latest_image_list,
            "latest_audios":latest_audio_list,
            
        }
        data["mixlir"] = mix

        return data, 200


#this is the daily verse endpoint 
@home.route("/daily_verse", methods=["POST", "PUT", "DELETE", "GET"])
def dail():
    if request.method == "POST":
        verse_title = request.json.get("verse_title")
        verse_body = request.json.get("verse_body")
        day_to_be_shown = request.json.get("day")
        month_to_be_shown = request.json.get("month")
        year_to_be_shown = request.json.get("year")
        img_url = request.json.get("image_url")
        verse_id  = request.json.get("_id")

        daily_verse_db.insert_one({
                                "_id":verse_id,
                                "verse_title":verse_title,
                                "verse_body":verse_body,
                                "day":day_to_be_shown,
                                "month":month_to_be_shown,
                                "year":year_to_be_shown,
                                "image_url": img_url
                                })
        
        return ({"message":"just uploaded successfully"}, 200)
    
    if request.method == "GET":
        all_verses = daily_verse_db.find()
        verse_list = []
        for verse in all_verses:
            verse_list.append(verse)
        
        return {"verse_list":verse_list}, 200

    if request.method == "PUT":
        info = request.json
        id = info.get("_id")
        keys = [i for i in info.keys()]
        data = {}
        for i in keys:
            if info.get(i) != "":
                data[i] = info.get(i)
        data.pop("_id")
        daily_verse_db.find_one_and_update({"_id":id}, {"$set":data})
        return {"message":"updated successfully"}, 200


    if request.method == "DELETE":
        args = request.args.get("_id")
        daily_verse_db.find_one_and_delete({"_id":args})
        return {"message":"verse deleted"}, 200
    

@home.route("/live_mixlir", methods=["GET", "POST", "PUT"])
def home_mixlir():
    
    item = mixlir_db.find_one()

    if request.method == "GET":
        return {"url": item["url"], "title": item["title"], "description":item["description"], "isLive":item["isLive"]}, 200

    if request.method == "POST":
        mixlir = request.json
        url = mixlir.get("mixlir_url")
        title = mixlir.get("mixlir_title")
        description = mixlir.get("description")
        isLive = mixlir.get("isLive")
        mixlir_db.insert_one({"url":url,
                              "title":title,
                              "description":description,
                              "isLive":isLive,
                              "date_uploaded": date_})
        return({"message":"uploaded successfully"}, 200)

    if request.method == "PUT":
        mixlir = request.json
        url = mixlir.get("mixlir_url")
        title = mixlir.get("mixlir_title")
        description = mixlir.get("description")
        isLive = mixlir.get("isLive")
        mixlir_db.find_one_and_update({"_id":ObjectId(item["_id"])},
                                      {"$set":{"url":url,
                                        "title":title,
                                        "description":description,
                                        "isLive":isLive,
                                        "date_uploaded": date_}})
        return({"message":"updated successfully"}, 200)









        



#for the themes 
