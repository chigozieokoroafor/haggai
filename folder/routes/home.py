from flask import Blueprint
from datetime import datetime

from flask import request
from bson import ObjectId 
from folder.database import daily_verse_db, devotion_list_db, mixlir_db, audio_db, image_db
from folder.functions import check_for_zero, check_date

import pymongo
# create extra endpoints for the daily verses to ad
home = Blueprint("home", __name__, url_prefix="/home")

date = datetime.utcnow()
date_ = date.strftime("%Y-%m-%d %H:%M:%S" ) 

@home.route("/")
def base():
    return "this is the home"


@home.route("/today_bible_verse", methods=["GET", "POST"])
def bible_verse():
    
    if request.method == "GET":
        try:
            verse = daily_verse_db.find_one({"day": str(check_for_zero(date.day)),
                                                "year": str(date.year),
                                                "month": str(check_for_zero(date.month))})
            verse["_id"] = str(ObjectId(verse["_id"]))
            return (verse, 200)

            
        except TypeError:
            return ({"message":"No verse for the day", "type":"error"}, 400)



    if request.method == "POST":
        verse_title = request.json.get("verse_title")
        verse_body = request.json.get("verse_body")
        day_to_be_shown = request.json.get("day_to_be_shown")
        month_to_be_shown = request.json.get("month_to_be_shown")
        year_to_be_shown = request.json.get("year_to_be_shown")
        img_url = request.json.get("image_url")

        daily_verse_db.insert_one({
                                "verse_title":verse_title,
                                "verse_body":verse_body,
                                "day":day_to_be_shown,
                                "month":month_to_be_shown,
                                "year":year_to_be_shown,
                                "image_url": img_url
                                })
        
        return ({"message":"just uploaded successfully", "type":"static"}, 200)


@home.route("/devotions", methods=["GET", "POST"])
def home_devotions():
    
    
    L =[]
    if request.method == "GET":
        try:
            dev_id = request.args["devotion_id"]
            dev_list = dev_id.split(", ")
            #print(dev_list)
            if len(dev_list)>1:
                for _id in dev_list:
                    devotion =devotion_list_db.find_one({"id":_id})
                    L.append({"Devotion Name": devotion["name"],
                            "Devotion Description":devotion["description"],
                            "Devotion Type": devotion["type"]})
                
                return ({"items":L, "type":"success"}, 200)
            
            elif len(dev_list)==1:
                devotion = devotion_list_db.find_one({"id":dev_id})
                return ({"Devotion Name": devotion["name"],
                        "Devotion Description":devotion["description"],
                        "Devotion Type": devotion["type"],
                        "type":"success"}, 200)  
        except:
            return ({"message":"no devotion_id provided", "type":"error"}, 400) 
        


    if request.method == "POST":
        return ({"message":"work in progress", "type":"static"}, 204)


#there should be a maximum of 5 videos in this Db
@home.route("/live_videos", methods= ["GET", "PUT"])
def live_video():
    
    
    if request.method == "GET":
        videos = videos.find()
        video_list = []
        for video_ in videos:
            video_list.append({"live_video_url":video_["url"],
                    "live_video_name":video_["name"],
                    "isLive":True})
        return {"items":video_list}, 200
        
    if request.method == "PUT":
        try:
            url=  request.json.get("video_url")
            name = request.json.get("video_name")
            isLive = request.json.get("isLive")
            

            if url==None or name==None or isLive==None:
                return ({"message":"nothing was provided"}, 400)

            else:
                for video_info in videos.find():
                    if check_date(video_info["datetime"]) == True:
                        videos.find_one_and_delete(video_info)
                            
                if videos.count_documents({})<5:
                    item = {"name":name, "url":url, "datetime":date_, "isLive":isLive}
                    videos.insert_one(item)
                    return({"message":"added successfully"}, 200)
                else:
                    return ({"message":"maximum items reached"}, 400)
                        
            

        except AttributeError:
            return {"message":"Something went wrong"}, 400



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

@home.route("/audio", methods=["GET"])
def home_audio():
    if request.method == "GET":
        data = audio_db.find().sort("rank", pymongo.DESCENDING).limit(5)
        data_ = []
        for item in data:
            d = {}
            d["audio_name"] = item["audio_name"]
            d["audio_url"] = item["audio_url"]
            d["rank"] = item["rank"]
            d["parent_folder"] = item["parent_folder"]
            data_.append(d)
        return {"items":data_}, 200

@home.route("/sermon_notes", methods=["GET"])
def home_sermon():
    info = request.json
    return {"message":"in progress"}, 200



@home.route("/images", methods=["GET"])
def home_images():
    images = image_db.find()
    return {"message":"in progress"}, 200








        



#for the themes 
