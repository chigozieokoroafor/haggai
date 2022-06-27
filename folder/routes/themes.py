from flask import Blueprint, request
import pymongo 
from folder.database import theme_db
from bson import ObjectId
from datetime import datetime



theme = Blueprint("themes", __name__, url_prefix="/api/haggai/theme")

date = datetime.utcnow()
date_ = date.strftime("%Y-%m-%d %H:%M:%S" ) 

@theme.route("/", methods=["POST", "GET", "PUT", "DELETE"])
def themes():
    theme_list_ = []
    if request.method == "GET":
        
        theme_list = theme_db.find().sort("rank", pymongo.DESCENDING)

        for theme_ in theme_list:

            theme_list_.append(theme_)
        
        return ({"items":theme_list_}, 200)
        
    if request.method == "POST":
        theme_ = request.json
        theme_url_light = theme_.get("light_url")
        theme_url_dark = theme_.get("dark_url")
        theme_name = theme_.get("name")
        #theme_rank = theme_.get("Rank")
        

        info_dict = {}
        keys = [i for i in theme_.keys()]
        #print(keys)
        for i in keys:
            info_dict[i] = theme_.get(str(i))
        info_dict["rank"] = int(str(theme_db.count_documents({}))+"0")+10
        info_dict["date_uploaded"] = date_
        #print(info_dict)
        theme_db.insert_one(info_dict)
        #theme_db.insert_one({"light_image_url":theme_url_light,"dark_image_url":theme_url_dark,"theme_name":theme_name,"rank":int(str(theme_db.count_documents({}))+"0")+10,"date_uploaded":date_uploaded})
        return {"message":"theme uploaded"}, 200
    
    if request.method == "PUT":
        info = request.json 
        id  = info.get("_id")
        info_dict = {}
        keys = [i for i in info.keys()]
        
        for i in keys:
            info_dict[i] = info.get(str(i))

        for key in keys:
            if info_dict[key] == "":
                info_dict.pop(key)
        info_dict.pop("_id")
        theme_db.find_one_and_update({"_id":id}, {"$set":info_dict})

        return {"message":"Theme Updated"}, 200

    if request.method == "DELETE":
        id = request.args.get("_id")
        theme_db.find_one_and_delete({"_id":id})
        return {"message":"Theme Deleted"}, 200

