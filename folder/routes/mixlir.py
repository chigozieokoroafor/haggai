from flask import Blueprint
from folder.database import mixlir_db
from flask import request
#from bson import ObjectId


mixlir = Blueprint("mixlir", __name__, url_prefix="/api/haggai")

@mixlir.route("/live_mixlir", methods=["GET", "POST", "PUT", "DELETE"])
def home_mixlir():
    
    if request.method == "GET":
        item = mixlir_db.find_one()
        if item == None:
            return {"mixlir":{}}, 200
        else:
            #item.pop("")
            return {"mixlir":item}, 200

    if request.method == "POST":
        info = request.json
        #url = mixlir.get("mixlir_url")
        #title = mixlir.get("mixlir_title")
        #description = mixlir.get("description")
        #isLive = mixlir.get("isLive")

        keys = [i for i in info.keys()]
        data = {}

        item = mixlir_db.find_one()
        for key in keys:
            data[key] = info.get(key)
        if item == None or item == {}:        
            mixlir_db.insert_one(data)
            message = "item uploaded successfully"
            return {"message":message}, 200
        else:
            message = "Existing Mixlir Available"
            return {"message":message}, 400
        
    if request.method == "PUT":
        info = request.json
        keys = [i for i in info.keys()]
        data = {}
        for key in keys:
            data[key] = info.get(key)

        for key in keys:
            if data[key] == "":
                data.pop(key)

        mixlir_db.find_one_and_update({"_id":data["_id"]},
                                      {"$set":data})

        return({"message":"updated successfully"}, 200)

    if request.method == "DELETE":
        args = request.args.get("_id")
        mixlir_db.find_one_and_delete({"_id":args})
        return {"message":"Mixlir Deleted"}, 200