from flask import Blueprint, request
import pymongo
from folder.database import devotion_list_db, devotion_types


devotions = Blueprint("devotions", __name__, url_prefix="/api/haggai")

@devotions.route("/")
def base():
    return "this is the devotions"

#for the devotions Screen 
@devotions.route("/devotions/<parent_id>", methods=["GET", "POST", "PUT", "DELETE"])
def devotion(parent_id):
    if request.method == "GET":
        args = request.args
        day = args.get("day")
        month = args.get("month")
        year = args.get("year")

        if parent_id != "_":

            d = devotion_types.find_one({"_id":parent_id})

            if d == None:
                return {"message":"Devotion items could not be found", "status":"error"}, 400
            else:
                isDaily = d["isDaily"]
                if isDaily == True:
                    devotion = devotion_list_db.find({"parent_id":parent_id, "month":int(month), "year":int(year)}).sort([("day", pymongo.DESCENDING)])

                    dev_list = []
                    for i in devotion:
                        dev_list.append(i)
                    return {"devotions":dev_list, "status":"success"}, 200

                if isDaily == False:
                    devotion = devotion_list_db.find({"parent_id":parent_id}).sort([("year", pymongo.DESCENDING),
                                                                                    ("month", pymongo.DESCENDING),
                                                                                    ("day", pymongo.DESCENDING)])
                    
                    dev_list = []
                    for i in devotion:
                        dev_list.append(i)
                
                    return {"devotions":dev_list, "status":"success"}, 200

                    

        
        if parent_id == "_":
            return {"message":"work in progress"}, 200
        

    if request.method == "POST":
        #------------- Day month year should be added ----------------- while uploading
        info = request.json
        keys = [i for i in info.keys()]        

        data = {}

        for key in keys:
            data[key] = info.get(key)

        try:
            id = data["_id"]
        except KeyError as e:
            return {"message":"_id not added. Kindly add _id parameter"}, 400
        
        try:
            if data["day"] == None:
                    return {"message":"Day not uploaded", "status":"error"}, 400
            if data["month"] == None:
                    return {"message":"Month not uploaded", "status":"error"}, 400
            if data["year"] == None:
                    return {"message":"Year not uploaded", "status":"error"}, 400
            data["rank"] = devotion_list_db.count_documents({}) * 10
            data["parent_id"] = parent_id

        except KeyError as e:
            return {"message": f"{e} parameter not added", "status":"error"}, 400
        


        check = devotion_list_db.find_one({"_id":id})
        if check == None:
            devotion_list_db.insert_one(data)
            return {"message":"Devotion uploaded", "status":"success"}, 200
        else:
            return {"message":"Document with preexisting id exists", "status":"error"}, 400


    if request.method == "PUT":
        info = request.json
        keys = [i for i in info.keys()]

        data = {}

        for key in keys:
            data[key] = info.get(key)
        
        for i in keys:
            if data[i] == "":
                data.pop(i)


        try:
            id = data["_id"]
            data.pop("_id")

            devotion_list_db.find_one_and_update({"_id":id}, {"$set":data})
            return {"message":"devotion uploaded", "status":"success"}, 200
        except KeyError as e:
            return {"message":"_id not added. Kindly add _id parameter", "status":"error"}, 400

    if request.method == "DELETE":
        id = request.args.get("_id")
        try:
            devotion_list_db.find_one_and_delete({"_id":id})
            return {"message":"devotion deleted", "status":"success"}, 200
        except:
            return {"message":"error occured during process", "status":"error"}, 400
    
# @devotions.route('/', methods=["GET"])
# def fetch_devotions():
#   try:
#     devotions = []
#     for devotion in devotion_collection.find():
#       devotion['_id'] = str(devotion['_id'])
#       devotions.append(devotion)
#     return ({ 'status': 'success', 'message': 'Devotions', 'devotions': devotions })
#   except Exception as e:
#     print('Error getting devotions')
#     return ({ 'status': 'error', 'message': str(e)})

