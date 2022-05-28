from flask import Blueprint, request
from folder.database import devotion_list_db


devotions = Blueprint("devotions", __name__, url_prefix="/api/haggai/devotion")

@devotions.route("/")
def base():
    return "this is the home"

#for the devotions Screen 
@devotions.route("/devotions/<parent_id>", methods=["GET", "POST"])
def devotion(parent_id):
    if request.method == "GET":
        d = devotion_list_db.find_one({"id":parent_id})
        if d:
            return("work in progress", 200)
        else: return "shit" 


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

