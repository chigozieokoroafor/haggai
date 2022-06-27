from flask import Blueprint, request
from folder.database import videos_db, latest_db
import pymongo
from pymongo.errors import DuplicateKeyError
video = Blueprint("videos", __name__, url_prefix="/api/haggai/video")



@video.route("/")
def base():
    return "this is the videos"

#note fist-fifth are going to be ids
@video.route("/Folder/<first>/<second>/<third>/<fourth>", methods=["POST", "PUT", "GET", "DELETE"])
def folder(first, second, third, fourth):
    if request.method == "POST":
        info = request.json
        id = info.get("id")
        keys = [i for i in info.keys()]
        data = {}
        for i in keys:
            data[i] = info.get(i)
        data["isFolder"] = True
        
        if data["is_finalFolder"]:
            pass
        else: data["is_finalFolder"] = False

        data["_id"] = id
        data.pop("id")
        
        #latest = info.get("latest")

        #latest_data = {}
        try:
            if first != "_":            
                folder = videos_db[first].find_one({"_id":id})
                if folder:
                    if second != "_" :
                        
                        folder = videos_db[first][second].find_one({"_id":id})
                        if folder:
                            if third != "_":
                                
                                folder = videos_db[first][second][third].find_one({"_id":id})
                                if folder:
                                    if fourth != "_":
                                    
                                        folder = videos_db[first][second][third][fourth].find_one({"_id":id})
                                        if folder:
                                                return {"message":"folder already exists", "status":"error"}, 400
                                        else:
                                            data["isFolder"] = True
                                            data["is_finalFolder"] = True
                                            data["_id"] = id
                                            videos_db[first][second][third][fourth].insert_one(data)
                                            
                                            return {"message":"Folder created", "status":"success"}, 200
                                    else:
                                        return {"message":"folder already exists", "status":"error"}, 400 
                                else:
                                    data["isFolder"] = True
                                    data["is_finalFolder"] = False
                                    data["_id"] = id
                                    videos_db[first][second][third].insert_one(data)
                                    
                                    return {"message":"Folder created", "status":"success"}, 200
                            else:
                                return {"message":"folder already exists", "status":"error"}, 400
                        else:
                            data["isFolder"] = True
                            data["is_finalFolder"] = False
                            data["_id"] = id
                            videos_db[first][second].insert_one(data)
                            
                            return {"message":"Folder created", "status":"success"}, 200

                    else:
                        return {"message":"folder already exists", "status":"error"}, 400
                else:
                    data["isFolder"] = True
                    data["is_finalFolder"] = False
                    data["_id"] = id
                    videos_db[first].insert_one(data)
                    
                    return {"message":"Folder created", "status":"success"}, 200
                
            else:
                data["isFolder"] = True
                data["is_finalFolder"] = False
                data["_id"] = id
                videos_db.insert_one(data)
                return {"message":"Folder created", "status":"success"}, 200
        except DuplicateKeyError:
            return {"message":"Item with existing id exists", "status":"error"}, 400

    if request.method == "PUT":
        info = request.json
        latest = info.get("latest")
        id = info.get("id")
        keys = [i for i in info.keys()]
        data={}
        for i in keys:
            data[i] = info.get(i)
        
        for i in keys:
            if data[i] == "":
                data.pop(i)

        #data.pop("latest")
        data.pop("id")
        try:
            if first != "_":
                if second != "_":
                    if third != "_":
                        if fourth != "_":
                            videos_db[first][second][third][fourth].find_one_and_update({"_id":id}, {"$set":data})
                            folders = videos_db[first][second][third][fourth].find({"isFolder":True})
                            folders_ = []
                            for folder in folders:
                                folders_.append(folder)
                            if latest != False:
                                latest_db.delete_many({"type":"video"})
                                latest_items = videos_db[first][second][third][fourth][id].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(30)
                                item = []
                                for items in latest_items:
                                    items["type"] = "image"
                                    items["parent_id"] = id
                                    items.pop("_id")
                                    item.append(items)
                                latest_db.delete_many({"type":"image"})
                                latest_db.insert_many(item)
                            else:
                                latest_db.delete_many({"parent_id":id})
                                latest_db.insert_many(item)
                            
                            return {"message":"folder updated", "folders":folders_}, 200
                        else:
                            videos_db[first][second][third].find_one_and_update({"_id":id}, {"$set":data})
                            folders = videos_db[first][second][third].find()
                            folders_ = []
                            for folder in folders:
                                folders_.append(folder)
                            if latest != False:
                                latest_db.delete_many({"type":"video"})
                                latest_items = videos_db[first][second][third][fourth][id].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(30)
                                item = []
                                for items in latest_items:
                                    items["type"] = "image"
                                    items["parent_id"] = id
                                    items.pop("_id")
                                    item.append(items)
                                latest_db.delete_many({"type":"image"})
                                latest_db.insert_many(item)
                            else:
                                latest_db.delete_many({"parent_id":id})
                            return {"message":"folder updated", "folders":folders_}, 200
                    else:
                        videos_db[first][second].find_one_and_update({"_id":id}, {"$set": data})
                        folders = videos_db[first][second].find()
                        folders_ = []
                        for folder in folders:
                            folders_.append(folder)
                        if latest != False:
                            latest_db.delete_many({"type":"video"})
                            latest_items = videos_db[first][second][third][fourth][id].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(30)
                            item = []
                            for items in latest_items:
                                items["type"] = "image"
                                items["parent_id"] = id
                                items.pop("_id")
                                item.append(items)
                            latest_db.delete_many({"type":"image"})
                            latest_db.insert_many(item)
                        else:
                            latest_db.delete_many({"parent_id":id})
                        return {"message":"folder updated", "folders":folders_}, 200
                else:
                    videos_db[first].find_one_and_update({"_id":id}, {"$set":data})
                    folders = videos_db[first].find()
                    folders_ = []
                    for folder in folders:
                        folders_.append(folder)
                    if latest != False:
                        latest_db.delete_many({"type":"video"})
                        latest_items = videos_db[first][second][third][fourth][id].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(30)
                        item = []
                        for items in latest_items:
                            items["type"] = "image"
                            items["parent_id"] = id
                            items.pop("_id")
                            item.append(items)
                        latest_db.delete_many({"type":"image"})
                        latest_db.insert_many(item)
                    else:
                        latest_db.delete_many({"parent_id":id})
                    return {"message":"folder updated", "folders":folders_}, 200    
            else:
                videos_db.find_one_and_update({"_id":id}, {"$set":data})
                folders = videos_db.find()
                folders_ = []
                for folder in folders:
                    folders_.append(folder)
                if latest != False:
                    latest_db.delete_many({"type":"video"})
                    latest_items = videos_db[first][second][third][fourth][id].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(30)
                    item = []
                    for items in latest_items:
                        items["type"] = "image"
                        items["parent_id"] = id
                        items.pop("_id")
                        item.append(items)
                    latest_db.delete_many({"type":"image"})
                    latest_db.insert_many(item)
                else:
                    latest_db.delete_many({"parent_id":id})
                return {"message":"folder updated", "folders":folders_}, 200
        except AttributeError :
            return {"message":"Folder Specified Cannot Be Found"}, 400
        except TypeError :
            return {"message":"Folder is empty"}, 400

    if request.method == "GET":
        page = request.args.get("page")
        skip_value = 30 * int(page)
        folder_list = []
        if first != "_":
            if second != "_":
                if third != "_":
                    if fourth != "_":
                            folders = videos_db[first][second][third][fourth].find({"isFolder":True}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                            for folder in folders:
                                folder["id"] = folder["_id"]
                                folder.pop("_id")
                                folder_list.append(folder)
                            return {"folders":folder_list}, 200
                    else:
                        folders = videos_db[first][second][third].find({"isFolder":True}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                        for folder in folders:
                            folder["id"] = folder["_id"]
                            folder.pop("_id")
                            folder_list.append(folder)
                        return {"folders":folder_list}, 200
                else:
                        folders = videos_db[first][second].find({"isFolder":True}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                        for folder in folders:
                            folder["id"] = folder["_id"]
                            folder.pop("_id")
                            folder_list.append(folder)
                        return {"folders":folder_list}, 200
            else:
                folders = videos_db[first].find({"isFolder":True}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                for folder in folders:
                    folder["id"] = folder["_id"]
                    folder.pop("_id")
                    folder_list.append(folder)                
                return {"folders":folder_list}, 200
        else:
            folders = videos_db.find({"isFolder":True}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
            for folder in folders:
                folder["id"] = folder["_id"]
                folder.pop("_id")
                folder_list.append(folder)
            return {"folders":folder_list}, 200
    

    if request.method == "DELETE":
        id = request.args.get("_id")
        folder_list = []
        if first != "_":
            if second != "_":
                if third != "_":
                    if fourth != "_":
                            videos_db[first][second][third][fourth].delete_one({"_id":id})
                            videos_db[first][second][third][fourth][id].drop()
                            updated_folders = videos_db[first][second][third][fourth].find()
                            for i in updated_folders:
                                folder_list.append(i)
                            return {"folders":folder_list}, 200
                    else:
                        videos_db[first][second][third].delete_one({"_id":id})
                        videos_db[first][second][third][id].drop()
                        updated_folders = videos_db[first][second][third].find()
                        for i in updated_folders:
                            folder_list.append(i)
                        return {"folders":folder_list}, 200
                else:
                        videos_db[first][second].delete_one({"_id":id})
                        videos_db[first][second][id].drop()
                        updated_folders = videos_db[first][second].find()
                        for i in updated_folders:
                            folder_list.append(i)
                        return {"folders":folder_list}, 200
            else:
                videos_db[first].delete_one({"_id":id})
                videos_db[first][id].drop()
                updated_folders = videos_db[first].find()
                for i in updated_folders:
                    folder_list.append(i)
                return {"folders":folder_list}, 200
        else:
            videos_db.delete_one({"_id":id})
            videos_db[id].drop()
            updated_folders = videos_db.find()
            for i in updated_folders:
                folder_list.append(i)
            return {"folders":folder_list}, 200


@video.route("Items/<first>/<second>/<third>/<fourth>/<fifth>", methods=["POST", "GET", "PUT", "DELETE"])
def items(first, second, third, fourth, fifth):
    if request.method == "POST":
        info = request.json
        #video_url = info.get("video_url")
        #video_name = info.get("video_name")
        #video_image = info.get("video_image")
        #timestamp = info.get("timestamp")
        id = info.get("id")
        #latest = info.get("latest")
        

        keys = [i for i in info.keys()]
        data = {}
        for i in keys:
            data[i] = info.get(i)
        data["isFolder"] = False
        data["_id"] = id
        data.pop("id")
        data.pop("latest")

        if first!= "_":
            if second != "_" :
                if third != "_" :
                    if fourth != "_":
                        if fifth != "_":
                            
                            videos_db[first][second][third][fourth][fifth].insert_one(data)
                            videos_db[first][second][third][fourth].find_one_and_update({"_id":fifth, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                            
                            return {"message":"uploaded successfuly"}, 200

                        else:
                            
                            videos_db[first][second][third][fourth].insert_one(data)
                            videos_db[first][second][third].find_one_and_update({"_id":fourth, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                            
                            return {"message":"uploaded successfully"},200
                    else:
                            
                        videos_db[first][second][third].insert_one(data)
                        videos_db[first][second].find_one_and_update({"_id":third, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                        
                        return {"message": "uploaded succesfully"}, 200
                else:
                            
                    videos_db[first][second].insert_one(data)  
                    videos_db[first].find_one_and_update({"_id":second, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                    
                    return{"message":"uploaded successfully"}, 200
            else:
                
                videos_db[first].insert_one(data)
                videos_db.find_one_and_update({"_id":first, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                
                return {"message":"uploaded successfully"}, 200
        else:
            return {"message":"No Folder Specified"}, 400

    if request.method == "GET":
        page = request.args.get("page")
        skip_value = 30 * int(page)
        doc_list=[]
        #live_videos = latest_db.find({"isLive":True})
        #latest_items = [live_video for live_video in live_videos]
        
        if first != "_":
            if second != "_":
                if third != "_":
                    if fourth != "_":
                        if fifth != "_":
                            documents = videos_db[first][second][third][fourth][fifth].find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                            for doc_ in documents :
                                doc_["id"] = doc_["_id"]
                                doc_.pop("_id")
                                doc_list.append(doc_)
                            return {"items":doc_list}, 200
                        else:
                            documents = videos_db[first][second][third][fourth].find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                            for doc_ in documents :
                                doc_["id"] = doc_["_id"]
                                doc_.pop("_id")
                                doc_list.append(doc_)
                            return {"items":doc_list}, 200
                    else:
                        documents = videos_db[first][second][third].find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                        for doc_ in documents :
                            doc_["id"] = doc_["_id"]
                            doc_.pop("_id")
                            doc_list.append(doc_)
                        return {"items":doc_list}, 200
                else:
                    documents = videos_db[first][second].find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                    for doc_ in documents :
                        doc_["id"] = doc_["_id"]
                        doc_.pop("_id")
                        doc_list.append(doc_)
                    return {"items":doc_list}, 200
            else:
                documents = videos_db[first].find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                for doc_ in documents :
                    doc_["id"] = doc_["_id"]
                    doc_.pop("_id")
                    doc_list.append(doc_)
                return {"items":doc_list}, 200
        else:
            documents = videos_db.find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
            for doc_ in documents :
                doc_["id"] = doc_["_id"]
                doc_.pop("_id")
                doc_list.append(doc_)
            return {"items":doc_list}, 200

    if request.method == "PUT":
        info = request.json
        id  = info.get("id")
        #latest = info.get("latest")
        keys = [i for i in info.keys()]
        data = {}
        for i in keys:
            if info.get(i) != "":
                data[i] = info.get(i)
        data.pop("id")
        #data.pop("latest")
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
        
    if request.method == "DELETE":
        id = request.args.get("_id")
        folder_list = []
        if first != "_":
            if second != "_":
                if third != "_":
                    if fourth != "_":
                            videos_db[first][second][third][fourth].delete_one({"_id":id})
                            #audio_db[first][second][third][fourth][id].drop()
                            updated_folders = videos_db[first][second][third][fourth].find({"isFolder":False})
                            for i in updated_folders:
                                folder_list.append(i)
                            return {"folders":folder_list}, 200
                    else:
                        videos_db[first][second][third].delete_one({"_id":id})
                        #audio_db[first][second][third][id].drop()
                        updated_folders = videos_db[first][second][third].find({"isFolder":False})
                        for i in updated_folders:
                            folder_list.append(i)
                        return {"folders":folder_list}, 200
                else:
                        videos_db[first][second].delete_one({"_id":id})
                        #audio_db[first][second][id].drop()
                        updated_folders = videos_db[first][second].find({"isFolder":False})
                        for i in updated_folders:
                            folder_list.append(i)
                        return {"folders":folder_list}, 200
            else:
                videos_db[first].delete_one({"_id":id})
                #audio_db[first][id].drop()
                updated_folders = videos_db[first].find({"isFolder":False})
                for i in updated_folders:
                    folder_list.append(i)
                return {"folders":folder_list}, 200
        else:
            videos_db.delete_one({"_id":id})
            #audio_db[id].drop()
            updated_folders = videos_db.find({"isFolder":False})
            for i in updated_folders:
                folder_list.append(i)
            return {"folders":folder_list}, 200
   

        




    