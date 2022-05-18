from datetime import datetime
from folder import app
from flask import request
from bson import ObjectId 
from folder.database import *
from folder import check_for_zero, date, date_, check_date # check_live
import pymongo

@app.route("/home/today_bible_verse", methods=["GET", "POST"])
def bible_verse():
    
    if request.method == "GET":
        try:
            verse = daily_verse_db.find_one({"day": str(check_for_zero(date.day)),
                                                #"year": str(check_for_zero(date.year)),
                                                "month": str(check_for_zero(date.month))})
            
            return ({"verse_of_the_day":verse["verse_body"], 
                         "verse_title":verse["verse_title"],
                         "day":verse["day"], 
                         "month":verse["month"],
                         "year": verse["year"],
                         "image_url":verse["image_url"],
                         "type":"success"}, 200)

            
        except TypeError:
            return ({"message":"No verse for the day", "type":"fail"}, 400)

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


@app.route("/home/devotions", methods=["GET", "POST"])
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
@app.route("/home/live_videos", methods= ["GET", "PUT"])
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



@app.route("/home/live_mixlir", methods=["GET", "POST", "PUT"])
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
        mixlir_db.find_one_and_update({"_id":ObjectId(item["_id"])},
                                      {"$set":{"url":url,
                                        "title":title,
                                        "description":description,
                                        "isLive":isLive,
                                        "date_uploaded": date_}})
        return({"message":"updated successfully"}, 200)

@app.route("/home/audio", methods=["GET"])
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

@app.route("/home/sermon_notes", methods=["GET"])
def home_sermon():
    info = request.json
    return {"message":"in progress"}, 200



@app.route("/home/images", methods=["GET"])
def home_images():
    images = image_db.find()
    return {"message":"in progress"}, 200


#for the devotions Screen 
@app.route("/devotions/<parent_id>", methods=["GET", "POST"])
def devotion(parent_id):
    if request.method == "GET":
        d = devotion_list_db.find_one({"id":parent_id})
        if d:
            return("work in progress", 200)
        else: return "shit" 




@app.route("/audio/<first_id>/<second_id>/<third_id>/<fourth_id>/<fifth_id>", methods=["POST", "GET"])
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


@app.route("/images/<first>/<second>/<third>/<fourth>/<fifth>", methods=["POST", "GET"])
def images(first, second, third, fourth, fifth):
    if request.method == "POST":
        info = request.json
        image_url = info.get("image_url")
        image_name = info.get("image_name")
        

        image_db.insert_one({"id":first, "final":False})
        if second != "_" :
            image_db[first].insert_one({"id":second, "final":False})
            if third != "_" :
                image_db[first][second].insert_one({"id":third, "final":False})
                if fourth != "_":
                    image_db[first][second][third].insert_one({"id":fourth, "final":False})
                    if fifth != "_":
                        image_db[first][second][third][fourth].insert_one({"id":fifth, "final":True})
                        image_db[first][second][third][fourth][fifth].insert_one({
                                                    "image_url":image_url,
                                                    "image_name":image_name, 
                                                    "rank":int(image_db[first][second][third][fourth][fifth].count_documents({}))+10
                                                        })
                        return {"message":"all were uploaded"}

                    else:
                        image_db[first][second][third].find_one_and_update({"id":fourth},{"$set":{"final":True}})
                        image_db[first][second][third][fourth].insert_one({
                                                            "image_url":image_url,
                                                            "image_name":image_name, 
                                                            "rank":int(image_db[first][second][third][fourth].count_documents({}))+10
                                                                })
                else:
                        image_db[first][second].find_one_and_update({"id":fourth},{"$set":{"final":True}})
                        image_db[first][second][third].insert_one({
                                                            "image_url":image_url,
                                                            "image_name":image_name, 
                                                            "rank":int(image_db[first][second][third].count_documents({}))+10
                                                                })
            else:
                        image_db[first].find_one_and_update({"id":fourth},{"$set":{"final":True}})
                        image_db[first][second].insert_one({
                                                            "image_url":image_url,
                                                            "image_name":image_name, 
                                                            "rank":int(image_db[first][second].count_documents({}))+10
                                                                })
                        return{"message":"some were upladed"}, 200
        else:
            image_db.find_one_and_update({"id":first},{"$set":{"final":True}})
            image_db[first].insert_one({
                                            "image_url":image_url,
                                            "image_name":image_name, 
                                            "rank":int(image_db[first].count_documents({}))+10
                                            })
            return {"message":"one was uplaoaded"}
    

    if request.method == "GET":
        doc_list=[]
        if first != "_":
            if second != "_":
                if third != "_":
                    if fourth != "_":
                        if fifth != "_":
                            documents = image_db[first][second][third][fourth][fifth].find().limit(15)
                            for doc_ in documents :
                                doc = {}
                                doc["image_url"] = doc_["image_url"]
                                doc["image_name"] = doc_["image_name"]
                                doc["rank"] = doc_["rank"]
                                doc_list.append(doc)
                            return {"items":doc_list}, 200
                        else:
                            documents = image_db[first][second][third][fourth].find().limit(15)
                            for doc_ in documents :
                                doc = {}
                                doc["image_url"] = doc_["image_url"]
                                doc["image_name"] = doc_["image_name"]
                                doc["rank"] = doc_["rank"]
                                doc_list.append(doc)
                            return {"items":doc_list}, 200
                    else:
                        documents = image_db[first][second][third][fourth][fifth].find().limit(15)
                        for doc_ in documents :
                            doc = {}
                            doc["image_url"] = doc_["image_url"]
                            doc["image_name"] = doc_["image_name"]
                            doc["rank"] = doc_["rank"]
                            doc_list.append(doc)
                        return {"items":doc_list}, 200
                else:
                    documents = image_db[first][second][third][fourth].find().limit(15)
                    for doc_ in documents :
                        doc = {}
                        doc["image_url"] = doc_["image_url"]
                        doc["image_name"] = doc_["image_name"]
                        doc["rank"] = doc_["rank"]
                        doc_list.append(doc)
                    return {"items":doc_list}, 200
            else:
                documents = image_db[first][second][third][fourth].find().limit(15)
                for doc_ in documents :
                    doc = {}
                    doc["image_url"] = doc_["image_url"]
                    doc["image_name"] = doc_["image_name"]
                    doc["rank"] = doc_["rank"]
                    doc_list.append(doc)
                return {"items":doc_list}, 200
        else:
            documents = image_db[first][second][third][fourth].find().limit(15)
            for doc_ in documents :
                doc = {}
                doc["image_url"] = doc_["image_url"]
                doc["image_name"] = doc_["image_name"]
                doc["rank"] = doc_["rank"]
                doc_list.append(doc)
            return {"items":doc_list}, 200



        



#for the themes 
@app.route("/themes", methods=["POST", "GET"])
def themes():
    if request.method == "GET":
        theme_list_ = []
        theme_list = theme_db.find().sort("rank", -1)
        for theme_ in theme_list:
            theme_list_.append({"name":theme_["theme_name"],
                                "dark_image_url":theme_["dark_image_url"],
                                "light_image_url":theme_["light_image_url"],
                                "rank":theme_["rank"]})
        
        return ({"items":theme_list_}, 200)
        
    if request.method == "POST":
        theme_ = request.json
        theme_url_light = theme_.get("light_url")
        theme_url_dark = theme_.get("dark_url")
        theme_name = theme_.get("name")
        theme_rank = theme_.get("Rank")
        date_uploaded = date_
        theme_db.insert_one({"light_image_url":theme_url_light,
                          "dark_image_url":theme_url_dark,
                          "theme_name":theme_name,
                          "rank":int(audio_db.count_documents({}))+10,
                          "date_uploaded":date_uploaded})

        return ({"message":"work in progress", "type":"static"}, 204)