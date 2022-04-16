#from email.mime import image
from flask import Blueprint, request
from folder.database import image_db
import pymongo

image = Blueprint("images", __name__, url_prefix="/images")

@image.route("/")
def base():
    return "this is the home"

@image.route("/images/<first>/<second>/<third>/<fourth>/<fifth>", methods=["POST", "GET"])
def images(first, second, third, fourth, fifth):
    if request.method == "POST":
        info = request.json
        image_url = info.get("image_url")
        image_name = info.get("image_name")
        
        if first!= "_":
            image_db.insert_one({
                            "name":first, 
                            "url":image_url, 
                            "folder":True,
                            "final_folder":False,
                            "rank":int(str(image_db.count_documents({}))+"0")+10})
            if second != "_" :
                image_db[first].insert_one({
                                            "name":second, 
                                            "url":image_url, 
                                            "folder":True,
                                            "final_folder":False,
                                            "rank":int(str(image_db[first].count_documents({}))+"0")+10 })
                if third != "_" :
                    image_db[first][second].insert_one({
                                                        "name":third, 
                                                        "url":image_url,
                                                        "folder":True,
                                                        "final_folder":False,
                                                        "rank":int(str(image_db[first][second].count_documents({}))+"0")+10})
                    if fourth != "_":
                        image_db[first][second][third].insert_one({
                                                                    "name":fourth, 
                                                                    "url":image_url,
                                                                    "folder":True,
                                                                    "final_folder":False,
                                                                    "rank":int(str(image_db[first][second][third].count_documents({}))+"0")+10})
                        if fifth != "_":
                            image_db[first][second][third][fourth].insert_one({
                                                                                "name":fifth, 
                                                                                "url":image_url, 
                                                                                "folder":True,
                                                                                "final_folder":True,
                                                                                "rank":int(str(image_db[first][second][third][fourth].count_documents({}))+"0")+10})
                            image_db[first][second][third][fourth][fifth].insert_one({
                                                        "url":image_url,
                                                        "name":image_name,
                                                        "folder":False, 
                                                        "final_folder":False,
                                                        "rank":int(str(image_db[first][second][third][fourth][fifth].count_documents({}))+"0")+10
                                                            })
                            return {"message":"uploaded successfuly"}, 200

                        else:
                            image_db[first][second][third][fourth].insert_one({
                                                                "url":image_url,
                                                                "name":image_name,
                                                                "folder":False, 
                                                                "final_folder":False,
                                                                "rank":int(str(image_db[first][second][third][fourth].count_documents({}))+"0")+10
                                                                    })
                            return {"message":"uploaded successfully"},200
                    else:
                            
                            image_db[first][second][third].insert_one({
                                                                "url":image_url,
                                                                "name":image_name,
                                                                "folder":False, 
                                                                "final_folder":False,
                                                                "rank":int(str(image_db[first][second][third].count_documents({}))+"0")+10
                                                                    })
                            return {"message": "uploaded succesfully"}, 200
                else:
                            
                            image_db[first][second].insert_one({
                                                                "url":image_url,
                                                                "name":image_name,
                                                                "folder":False, 
                                                                "final_folder":False,
                                                                "rank":int(str(image_db[first][second].count_documents({}))+"0")+10
                                                                    })
                            return{"message":"uploaded successfully"}, 200
            else:
                
                image_db[first].insert_one({    
                                            "url":image_url,
                                            "name":image_name, 
                                            "folder":False, 
                                            "final_folder":False,
                                            "rank":int(str(image_db[first].count_documents({}))+"0")+10
                                                })
                return {"message":"uploaded successfully"}, 200
    

    if request.method == "GET":
        doc_list=[]
        if first != "_":
            if second != "_":
                if third != "_":
                    if fourth != "_":
                        if fifth != "_":
                            documents = image_db[first][second][third][fourth][fifth].find().sort("rank", pymongo.DESCENDING).limit(15)
                            for doc_ in documents :
                                doc = {}
                                doc["url"] = doc_["url"]
                                doc["name"] = doc_["name"]
                                doc["rank"] = doc_["rank"]
                                doc["final_folder"] = doc_["folder"]
                                doc_list.append(doc)
                            return {"items":doc_list}, 200
                        else:
                            documents = image_db[first][second][third][fourth].find().sort("rank", pymongo.DESCENDING).limit(15)
                            for doc_ in documents :
                                doc = {}
                                doc["url"] = doc_["url"]
                                doc["name"] = doc_["name"]
                                doc["rank"] = doc_["rank"]
                                doc["folder"] = doc_["folder"]
                                doc_list.append(doc)
                            return {"items":doc_list}, 200
                    else:
                        documents = image_db[first][second][third].find().sort("rank", pymongo.DESCENDING).limit(15)
                        for doc_ in documents :
                                doc = {}
                                doc["url"] = doc_["url"]
                                doc["name"] = doc_["name"]
                                doc["rank"] = doc_["rank"]
                                doc["folder"] = doc_["folder"]
                                doc_list.append(doc)
                        return {"items":doc_list}, 200
                else:
                    documents = image_db[first][second].find().sort("rank", pymongo.DESCENDING).limit(15)
                    for doc_ in documents :
                                doc = {}
                                doc["url"] = doc_["url"]
                                doc["name"] = doc_["name"]
                                doc["rank"] = doc_["rank"]
                                doc["folder"] = doc_["folder"]
                                doc_list.append(doc)
                    return {"items":doc_list}, 200
            else:
                documents = image_db[first].find().sort("rank", pymongo.DESCENDING).limit(15)
                for doc_ in documents :
                                doc = {}
                                doc["url"] = doc_["url"]
                                doc["name"] = doc_["name"]
                                doc["rank"] = doc_["rank"]
                                doc["folder"] = doc_["folder"]
                                doc_list.append(doc)
                return {"items":doc_list}, 200
        else:
            documents = image_db.find().sort("rank", pymongo.DESCENDING).limit(15)
            for doc_ in documents :
                                doc = {}
                                doc["url"] = doc_["url"]
                                doc["name"] = doc_["name"]
                                doc["rank"] = doc_["rank"]
                                doc["folder"] = doc_["folder"]
                                doc_list.append(doc)
            return {"items":doc_list}, 200
