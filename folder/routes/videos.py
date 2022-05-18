from flask import Blueprint, request
from folder.database import videos_db, latest_db
import pymongo

video = Blueprint("videos", __name__, url_prefix="/videos")

@video.route("/")
def base():
    return "this is the videos"

@video.route("/makeFolder/<first>/<second>/<third>/<fourth>/<fifth>", methods=["POST"])
def makefolder(first, second, third, fourth, fifth):
    if request.method == "POST":
        info = request.json
        folder_image_url = info.get("folder_image_url")
        folder_name = info.get("folder_name")
        timestamp = info.get("timestamp")
        id = info.get("id")
        latest = info.get("latest")
        if first != "_":
            
            folder = videos_db.find_one({"_id":id})
            if folder:
                if second != "_" :
                    
                    folder = videos_db[first].find_one({"_id":id})
                    if folder:
                        if third != "_":
                            
                            folder = videos_db[first][second].find_one({"_id":id})
                            if folder:
                                if fourth != "_":
                                   
                                    folder = videos_db[first][second][third].find_one({"_id":id})
                                    if folder:
                                        if fifth != "_":
                                            folder = videos_db[first][second][third][fourth].find_one({"_id":id})
                                            if folder:
                                                return {"message":"folder exists"}, 400
                                            else:
                                                data = {"folder_name":folder_name,
                                                        "folder_image_url":folder_image_url,
                                                        "isFolder":True,
                                                        "type":"video",
                                                        "timestamp":timestamp,
                                                        "is_finalFolder": True,
                                                        "_id":id
                                                        }
                                                videos_db[first][second][third][fourth].insert_one(data)
                                                if latest != False:
                                                    latest_db.insert_one(data)

                                                return {"message":"folder created"}, 200
                                        else:
                                            return {"message":"folder already exists"}, 400
                                    else:
                                        data = {
                                                "folder_name":folder_name,
                                                "folder_image_url":folder_image_url,
                                                "isFolder":True,
                                                "is_finalFolder":False,
                                                "type":"video",
                                                "timestamp":timestamp,
                                                "_id" :id
                                                }
                                        videos_db[first][second][third].insert_one(data)
                                        if latest != False:
                                            latest_db.insert_one(data)
                                        return {"message":"folder created"}, 200
                                else:
                                    return {"message":"folder already exists"}, 400 
                            else:
                                data ={
                                        "folder_name":folder_name,
                                        "folder_image_url":folder_image_url,
                                        "isFolder":True,
                                        "is_finalFolder":False,
                                        "type":"video",
                                        "timestamp" :timestamp,
                                        "_id":id
                                        }
                                videos_db[first][second].insert_one(data)
                                if latest != False:
                                    latest_db.insert_one(data)
                                return {"message":"folder created"}, 200
                        else:
                            return {"message":"folder already exists"}, 400
                    else:
                        data = {
                                "folder_name":folder_name,
                                "folder_image_url":folder_image_url,
                                "isFolder":True,
                                "is_finalFolder":False,
                                "type":"video",
                                "timestamp":timestamp,
                                "_id":id
                                }
                        videos_db[first].insert_one(data)
                        if latest != False:
                            latest_db.insert_one(data)
                        return {"message":"folder created"}, 200

                else:
                    return {"message":"folder already exists"}, 400
            else:
                data = {
                        "folder_name":first,
                        "folder_image_url":folder_image_url,
                        "isFolder":True,
                        "is_finalFolder":False,
                        "type":"video",
                        "timestamp":timestamp,
                        "_id":id
                                     }
                videos_db.insert_one(data)
                if latest != False:
                    latest_db.insert_one(data)
                return {"message":"folder created"}, 200
        else:
            return "No Folder Created"

@video.route("addItems/<first>/<second>/<third>/<fourth>/<fifth>", methods=["POST"])
def additems(first, second, third, fourth, fifth):
    if request.method == "POST":
        info = request.json
        video_url = info.get("video_url")
        video_name = info.get("video_name")
        timestamp = info.get("timestamp")
        id = info.get("id")
        
        if first!= "_":
            if second != "_" :
                if third != "_" :
                    if fourth != "_":
                        if fifth != "_":
                            videos_db[first][second][third][fourth][fifth].insert_one({
                                                        "url":video_url,
                                                        "name":video_name,
                                                        "isFolder":False,
                                                        "_id":id,
                                                        "timestamp":timestamp
                                                            })
                            videos_db[first][second][third][fourth].find_one_and_update({"_id":fifth}, {"$set":{"is_finalFolder":True}})
                            return {"message":"uploaded successfuly"}, 200

                        else:
                            videos_db[first][second][third][fourth].insert_one({
                                                                "url":video_url,
                                                                "name":video_name,
                                                                "isFolder":False, 
                                                                "_id":id,
                                                                "timestamp":timestamp
                                                                    })
                            videos_db[first][second][third].find_one_and_update({"_id":fourth}, {"$set":{"is_finalFolder":True}})
                            return {"message":"uploaded successfully"},200
                    else:
                            
                        videos_db[first][second][third].insert_one({
                                                                "url":video_url,
                                                                "name":video_name,
                                                                "isFolder":False, 
                                                                "_id":id,
                                                                "timestamp":timestamp
                                                                    })
                        videos_db[first][second].find_one_and_update({"_id":third}, {"$set":{"is_finalFolder":True}})
                        return {"message": "uploaded succesfully"}, 200
                else:
                            
                    videos_db[first][second].insert_one({
                                                        "url":video_url,
                                                        "name":video_name,
                                                        "isFolder":False, 
                                                        "_id":id,
                                                        "timestamp":timestamp
                                                        })  
                    videos_db[first].find_one_and_update({"_id":second}, {"$set":{"is_finalFolder":True}})
                    return{"message":"uploaded successfully"}, 200
            else:
                
                videos_db[first].insert_one({    
                                            "url":video_url,
                                            "name":video_name, 
                                            "isFolder":False, 
                                            "_id":id,
                                            "timestamp":timestamp
                                                })
                videos_db.find_one_and_update({"_id":first}, {"$set":{"is_finalFolder":True}})
                return {"message":"uploaded successfully"}, 200
        else:
            return {"message":"No Folder Specified"}, 400

@video.route("/getVideos/<first>/<second>/<third>/<fourth>/<fifth>", methods=["GET"])
def getvideos(first, second, third, fourth, fifth):
    if request.method == "GET":
        doc_list=[]
        if first != "_":
            if second != "_":
                if third != "_":
                    if fourth != "_":
                        if fifth != "_":
                            documents = videos_db[first][second][third][fourth][fifth].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(15)
                            for doc_ in documents :
                                doc_["id"] = doc_["_id"]
                                doc_.pop("_id")
                                doc_list.append(doc_)
                            return {"items":doc_list}, 200
                        else:
                            documents = videos_db[first][second][third][fourth].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(15)
                            for doc_ in documents :
                                doc_["id"] = doc_["_id"]
                                doc_.pop("_id")
                                doc_list.append(doc_)
                            return {"items":doc_list}, 200
                    else:
                        documents = videos_db[first][second][third].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(15)
                        for doc_ in documents :
                            doc_["id"] = doc_["_id"]
                            doc_.pop("_id")
                            doc_list.append(doc_)
                        return {"items":doc_list}, 200
                else:
                    documents = videos_db[first][second].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(15)
                    for doc_ in documents :
                        doc_["id"] = doc_["_id"]
                        doc_.pop("_id")
                        doc_list.append(doc_)
                    return {"items":doc_list}, 200
            else:
                documents = videos_db[first].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(15)
                for doc_ in documents :
                    doc_["id"] = doc_["_id"]
                    doc_.pop("_id")
                    doc_list.append(doc_)
                return {"items":doc_list}, 200
        else:
            documents = videos_db.find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(15)
            for doc_ in documents :
                doc_["id"] = doc_["_id"]
                doc_.pop("_id")
                doc_list.append(doc_)
            return {"items":doc_list}, 200

@video.route("/getFolders/<first>/<second>/<third>/<fourth>", methods=["GET"])
def getfolders(first, second, third, fourth):
    folder_list = []
    if first != "_":
        if second != "_":
            if third != "_":
                if fourth != "_":
                        folders = videos_db[first][second][third][fourth].find({"isFolder":True}).sort("timestamp")
                        for folder in folders:
                            folder["id"] = folder["_id"]
                            folder.pop("_id")
                            folder_list.append(folder)
                        return {"folders":folder_list}, 200
                else:
                    folders = videos_db[first][second][third].find({"isFolder":True}).sort("timestamp")
                    for folder in folders:
                        folder["id"] = folder["_id"]
                        folder.pop("_id")
                        folder_list.append(folder)
                    return {"folders":folder_list}, 200
            else:
                    folders = videos_db[first][second].find({"isFolder":True}).sort("timestamp")
                    for folder in folders:
                        folder["id"] = folder["_id"]
                        folder.pop("_id")
                        folder_list.append(folder)
                    return {"folders":folder_list}, 200
        else:
            folders = videos_db[first].find({"isFolder":True}).sort("timestamp")
            for folder in folders:
                folder["id"] = folder["_id"]
                folder.pop("_id")
                folder_list.append(folder)                
            return {"folders":folder_list}, 200
    else:
        folders = videos_db.find({"isFolder":True}).sort("timestamp")
        for folder in folders:
            folder["id"] = folder["_id"]
            folder.pop("_id")
            folder_list.append(folder)
        return {"folders":folder_list}, 200

@video.route("/updateFolders/<first>/<second>/<third>/<fourth>/<fifth>", methods=["PUT"])
def updatef(first, second, third, fourth, fifth):
    info = request.json
    latest = info.get("latest")
    keys = [i for i in info.keys()]
    data={}
    for i in keys:
        data[i] = info.get(i)
    data.pop("latest")
    for i in keys:
        if data[i] == "":
            data.pop(i)

    try:
        if first != "_":
            if second != "_":
                if third != "_":
                    if fourth != "_":
                        videos_db[first][second][third][fourth].find_one_and_update({"_id":fifth}, {"$set":data})
                        folders = videos_db[first][second][third][fourth].find({"isFolder":True})
                        folders_ = []
                        for folder in folders:
                            folders_.append(folder)
                        if latest != False:
                            latest_folder = videos_db[first][second][third][fourth].find_one({"_id":fifth})
                            latest_db.insert_one(latest_folder)
                        return {"message":"folder updated", "folders":folders_}, 200
                    else:
                        videos_db[first][second][third].find_one_and_update({"_id":fourth}, {"$set":data})
                        folders = videos_db[first][second][third].find()
                        folders_ = []
                        for folder in folders:
                            folders_.append(folder)
                        if latest != False:
                            latest_folder = videos_db[first][second][third].find_one({"_id":fourth})
                            latest_db.insert_one(latest_folder)
                        return {"message":"folder updated", "folders":folders_}, 200
                else:
                    videos_db[first][second].find_one_and_update({"_id":third}, {"$set": data})
                    folders = videos_db[first][second].find()
                    folders_ = []
                    for folder in folders:
                        folders_.append(folder)
                    if latest != False:
                        latest_folder = videos_db[first][second].find_one({"_id":third})
                        latest_db.insert_one(latest_folder)
                    return {"message":"folder updated", "folders":folders_}, 200
            else:
                videos_db[first].find_one_and_update({"_id":second}, {"$set":data})
                folders = videos_db[first].find()
                folders_ = []
                for folder in folders:
                    folders_.append(folder)
                if latest != False:
                    latest_folder = videos_db[first].find_one({"_id":second})
                    latest_db.insert_one(latest_folder)
                return {"message":"folder updated", "folders":folders_}, 200    
        else:
            videos_db.find_one_and_update({"_id":first}, {"$set":data})
            folders = videos_db.find()
            folders_ = []
            for folder in folders:
                folders_.append(folder)
            if latest != False:
                latest_folder = videos_db.find_one({"_id":first})
                latest_db.insert_one(latest_folder)
            return {"message":"folder updated", "folders":folders_}, 200
    except AttributeError :
        return {"message":"Folder Specified Cannot Be Found"}, 400


@video.route("/updateDocument/<first>/<second>/<third>/<fourth>/<fifth>", methods=["PUT"])
def updateD(first, second, third, fourth, fifth):
    info = request.json
    id  = info.get("id")
    keys = [i for i in info.keys()]
    data = {}
    for i in keys:
        if info.get(i) != "":
            data[i] = info.get(i)
    data.pop("id")
    doc_list = []
    try:
        if first != "_":
            if second != "_":
                if third != "_":
                    if fourth != "_":
                        if fifth != "_":
                            videos_db[first][second][third][fourth][fifth].find_one_and_update({"_id":id}, {"$set":data})
                            lis = videos_db[first][second][third][fourth][fifth].find()
                            for lis_ in lis:
                                lis_["id"] = lis_["_id"]
                                lis_.pop("_id")
                                doc_list.append(lis_)
                            return {"message":"Document updated successfully", "videos":doc_list}, 200
                        else:
                            videos_db[first][second][third][fourth].find_one_and_update({"_id":id}, {"$set":data})
                            lis = videos_db[first][second][third][fourth].find()
                            for lis_ in lis:
                                lis_["id"] = lis_["_id"]
                                lis_.pop("_id")
                                doc_list.append(lis_)
                            return {"message":"Document updated successfully", "videos":doc_list}, 200
                    else:
                        videos_db[first][second][third].find_one_and_update({"_id":id}, {"$set":data})
                        lis = videos_db[first][second][third].find()
                        for lis_ in lis:
                            lis_["id"] = lis_["_id"]
                            lis_.pop("_id")
                            doc_list.append(lis_)
                        return {"message":"Document updated successfully", "vidoes":doc_list}, 200
                else:
                    videos_db[first][second].find_one_and_update({"_id":id}, {"$set":data})
                    lis = videos_db[first][second].find()
                    for lis_ in lis:
                        lis_["id"] = lis_["_id"]
                        lis_.pop("_id")
                        doc_list.append(lis_)
                    return {"message":"Document updated successfully", "videos":doc_list}, 200
            else:
                videos_db[first].find_one_and_update({"_id":id}, {"$set":data})
                lis = videos_db[first].find()
                for lis_ in lis:
                    lis_["id"] = lis_["_id"]
                    lis_.pop("_id")
                    doc_list.append(lis_)
                return {"message":"Document updated successfully", "videos":doc_list}, 200
        else:
            return {"message":"No documents to update"}, 200
    except AttributeError:
        return {"message":"Incorrect Document ID passed"}, 400