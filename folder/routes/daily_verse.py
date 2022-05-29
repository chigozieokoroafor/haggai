from flask import Blueprint, request
from folder.database import daily_verse_db

verse = Blueprint("daily_verse", __name__, url_prefix="/api/v1/haggai")

#this is the daily verse endpoint 
@verse.route("/daily_verse", methods=["POST", "PUT", "DELETE", "GET"])
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
        
        return ({"message":"uploaded successfully"}, 200)
    
    if request.method == "GET":
        all_verses = daily_verse_db.find()
        limit = request.args.get("limit")
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
        update = daily_verse_db.find_one({"_id":id})
        return {"message":"updated successfully", "verse":update}, 200


    if request.method == "DELETE":
        args = request.args.get("_id")
        daily_verse_db.find_one_and_delete({"_id":args})
        items = daily_verse_db.find()
        item_list = [i for i in items]
        return {"message":"verse deleted", "items":item_list}, 200
