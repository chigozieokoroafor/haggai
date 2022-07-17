from flask import Blueprint, request
from folder.database import devotion_list_db


devotions = Blueprint("devotions", __name__, url_prefix="/api/haggai")

@devotions.route("/")
def base():
    return "this is the devotions"

#for the devotions Screen 
@devotions.route("/devotions/<parent_id>", methods=["GET", "POST", "PUT", "DELETE"])
def devotion(parent_id):
    if request.method == "GET":
        if parent_id != "_":
            d = devotion_list_db.find_one({"id":parent_id})
            if d:
                return("work in progress", 200)
            else: return "shit" 
        
        if parent_id == "_":
            return {"message":"work in progress"}, 200
        

    if request.method == "POST":
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
            is_lesson = data["isLesson"]
        except KeyError as e:
            return {"message": "isLesson not added, kindly add isLesson parameter"}, 400
        
        check = devotion_list_db.find_one({"_id":id})
        if check == None:
            devotion_list_db.insert_one(data)
            return {"message":"Devotion uploaded"}, 200
        else:
            return {"message":"Document with preexisting id exists"}, 400

    if request.method == "PUT":
        pass


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

