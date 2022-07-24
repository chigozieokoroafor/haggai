from flask import Blueprint
from flask import request
import pymongo
from folder.database import sermon_db

sermons = Blueprint("sermons", __name__, url_prefix="/api/haggai")

@sermons.route("/sermon", methods = ["GET", "POST", "PUT", "DELETE"])
def sermon():
    if request.method == "GET":
        page = int(request.args.get("page"))
        offset = page * 30

        all_sermons = sermon_db.find().skip(offset).limit(30).sort("timestamp", pymongo.DESCENDING)
        sermons = [i for i in all_sermons]
        sotw = sermon_db.find_one({"sermon_of_the_week":True})
        if sotw == None:
            sotw_ = {}
        else:
            sotw_ = sotw

        return {"sermon_list":sermons, "sermon_of_the_week":sotw_}, 200
        
    if request.method == "POST":
        info = request.json
        #week_sermon = info.get("sermon_of_the_week")

        keys = [i for i in info.keys()]
        data = {}

        for i in keys:
            data[i] = info.get(i)

        sermon_db.insert_one(data)
        new_items = sermon_db.find()
        item_list = [i for i in new_items]

        return {"message":"sermon added", "sermons":item_list}, 200
    
    if request.method == "PUT":
        info = request.json
        id  = info.get("_id")

        keys = [i for i in info.keys()]

        data = {}

        for i in keys:
            data[i] = info.get(i)
        
        for key in keys:
            if data[key] == "":
                data.pop(key)
                
        data.pop("_id")
        
        sermon_db.find_one_and_update({"_id":id}, {"$set":data})
        item = sermon_db.find_one({"_id":id})

        return {"message":"item updated", "sermons":item}, 200

    if request.method == "DELETE":
        args = request.args.get("_id")
        sermon_db.find_one_and_delete({"_id":args})
        new_items = sermon_db.find()
        item_list = [i for i in new_items]
        return {"message":"Item deleted", "sermons":item_list}, 200
        
