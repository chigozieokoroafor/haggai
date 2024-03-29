from email.errors import InvalidMultipartContentTransferEncodingDefect
from flask import Blueprint, request
from folder.database import image_db, latest_db
import pymongo

image = Blueprint("images", __name__, url_prefix="/api/haggai/image")

latest_image_items = []

@image.route("/")
def base():
    return "this is the images"

#make folders 
#add items
#update items
#remove items

# there should be something called IMAGE OF THE WEEK
# remember to comment  out the part of setting folders to finalfolders  and move to when documents are being uploaded 
# to make folders
@image.route("/Folder/<first>/<second>/<third>/<fourth>", methods=["POST", "PUT", "GET", "DELETE"])
def folder(first, second, third, fourth):
    if request.method == "POST":
        info = request.json
        #folder_image_url = info.get("image_url")
        #folder_name = info.get("name")
        #timestamp = info.get("timestamp")
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
        #data.pop("latest")

        
        if first != "_":            
            folder = image_db[first].find_one({"_id":id})
            if folder:
                if second != "_" :
                    
                    folder = image_db[first][second].find_one({"_id":id})
                    if folder:
                        if third != "_":
                            
                            folder = image_db[first][second][third].find_one({"_id":id})
                            if folder:
                                if fourth != "_":
                                   
                                    folder = image_db[first][second][third][fourth].find_one({"_id":id})
                                    if folder:
                                            return {"message":"folder already exists", "status":"error"}, 400
                                    else:
                                        image_db[first][second][third][fourth].insert_one(data)
                                        
                                        return {"message":"Folder created", "status":"success"}, 200
                                else:
                                    return {"message":"folder already exists", "status":"error"}, 400 
                            else:
                                image_db[first][second][third].insert_one(data)
                                
                                return {"message":"Folder created", "status":"success"}, 200
                        else:
                            return {"message":"folder already exists", "status":"error"}, 400
                    else:
                        image_db[first][second].insert_one(data)
                        
                        return {"message":"Folder created", "status":"success"}, 200

                else:
                    return {"message":"folder already exists", "status":"error"}, 400
            else:
                image_db[first].insert_one(data)
                
                return {"message":"Folder created", "status":"success"}, 200
            
        else:
            image_db.insert_one(data)
            return {"message":"Folder created", "status":"success"}, 200

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
                            image_db[first][second][third][fourth].find_one_and_update({"_id":id}, {"$set":data})
                            folders = image_db[first][second][third][fourth].find({"isFolder":True})
                            folders_ = []
                            for folder in folders:
                                folders_.append(folder)
                            if latest != False:
                                latest_db.delete_many({"type":"video"})
                                latest_items = image_db[first][second][third][fourth][id].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(30)
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
                            image_db[first][second][third].find_one_and_update({"_id":id}, {"$set":data})
                            folders = image_db[first][second][third].find()
                            folders_ = []
                            for folder in folders:
                                folders_.append(folder)
                            if latest != False:
                                latest_db.delete_many({"type":"video"})
                                latest_items = image_db[first][second][third][id].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(15)
                                item = []
                                for items in latest_items:
                                    items["type"] = "image"
                                    items["parent_id"] = id
                                    items.pop("_id")
                                latest_db.delete_many({"type":"image"})   
                                latest_db.insert_many(item)
                            else:
                                latest_db.delete_many({"parent_id":id})
                            return {"message":"folder updated", "folders":folders_}, 200
                    else:
                        image_db[first][second].find_one_and_update({"_id":id}, {"$set": data})
                        folders = image_db[first][second].find()
                        folders_ = []
                        for folder in folders:
                            folders_.append(folder)
                        if latest != False:
                            latest_db.delete_many({"type":"video"})
                            latest_items = image_db[first][second][id].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(15)
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
                    image_db[first].find_one_and_update({"_id":id}, {"$set":data})
                    folders = image_db[first].find()
                    folders_ = []
                    for folder in folders:
                        folders_.append(folder)
                    if latest != False:
                        latest_db.delete_many({"type":"video"})
                        latest_items = image_db[first][id].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(15)
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
                image_db.find_one_and_update({"_id":id}, {"$set":data})
                folders = image_db.find()
                folders_ = []
                for folder in folders:
                    folders_.append(folder)
                if latest != False:
                    latest_db.delete_many({"type":"video"})
                    latest_items = image_db[id].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(15)
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
                            folders = image_db[first][second][third][fourth].find({"isFolder":True}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                            for folder in folders:
                                folder["id"] = folder["_id"]
                                folder.pop("_id")
                                folder_list.append(folder)
                            return {"folders":folder_list}, 200
                    else:
                        folders = image_db[first][second][third].find({"isFolder":True}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                        for folder in folders:
                            folder["id"] = folder["_id"]
                            folder.pop("_id")
                            folder_list.append(folder)
                        return {"folders":folder_list}, 200
                else:
                        folders = image_db[first][second].find({"isFolder":True}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                        for folder in folders:
                            folder["id"] = folder["_id"]
                            folder.pop("_id")
                            folder_list.append(folder)
                        return {"folders":folder_list}, 200
            else:
                folders = image_db[first].find({"isFolder":True}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                for folder in folders:
                    folder["id"] = folder["_id"]
                    folder.pop("_id")
                    folder_list.append(folder)                
                return {"folders":folder_list}, 200
        else:
            folders = image_db.find({"isFolder":True}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
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
                            image_db[first][second][third][fourth].delete_one({"_id":id})
                            image_db[first][second][third][fourth][id].drop()
                            updated_folders = image_db[first][second][third][fourth].find()
                            for i in updated_folders:
                                folder_list.append(i)
                            return {"folders":folder_list}, 200
                    else:
                        image_db[first][second][third].delete_one({"_id":id})
                        image_db[first][second][third][id].drop()
                        updated_folders = image_db[first][second][third].find()
                        for i in updated_folders:
                            folder_list.append(i)
                        return {"folders":folder_list}, 200
                else:
                        image_db[first][second].delete_one({"_id":id})
                        image_db[first][second][id].drop()
                        updated_folders = image_db[first][second].find()
                        for i in updated_folders:
                            folder_list.append(i)
                        return {"folders":folder_list}, 200
            else:
                image_db[first].delete_one({"_id":id})
                image_db[first][id].drop()
                updated_folders = image_db[first].find()
                for i in updated_folders:
                    folder_list.append(i)
                return {"folders":folder_list}, 200
        else:
            image_db.delete_one({"_id":id})
            image_db[id].drop()
            updated_folders = image_db.find()
            for i in updated_folders:
                folder_list.append(i)
            return {"folders":folder_list}, 200


@image.route("Items/<first>/<second>/<third>/<fourth>/<fifth>", methods=["POST", "GET", "PUT", "DELETE"])
def items(first, second, third, fourth, fifth):
    if request.method == "POST":
        info = request.json
        #video_url = info.get("image_url")
        #video_name = info.get("image_name")
        #timestamp = info.get("timestamp")
        id = info.get("id")
        latest = info.get("latest")
        
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
                            image_db[first][second][third][fourth][fifth].insert_one(data)
                            image_db[first][second][third][fourth].find_one_and_update({"_id":fifth, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                            if latest == True:
                                latest_db.delete_many({"type":"image"})
                                data = image_db[first][second][third][fourth][fifth].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(5)
                                data_list = []
                                for item in data:
                                    item["type"] = "image"
                                    
                                    data_list.append(item)
                                latest_db.insert_many(data_list)
                            return {"message":"uploaded successfuly"}, 200

                        else:
                            image_db[first][second][third][fourth].insert_one(data)
                            image_db[first][second][third].find_one_and_update({"_id":fourth, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                            if latest == True:
                                latest_db.delete_many({"type":"image"})
                                data = image_db[first][second][third][fourth].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(5)
                                data_list = []
                                for item in data:
                                    item["type"] = "image"
                                    
                                    data_list.append(item)
                                latest_db.insert_many(data_list)
                            return {"message":"uploaded successfully"},200
                    else:
                            
                        image_db[first][second][third].insert_one(data)
                        image_db[first][second].find_one_and_update({"_id":third, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                        if latest == True:
                            latest_db.delete_many({"type":"image"})
                            data = image_db[first][second][third].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(5)
                            data_list = []
                            for item in data:
                                
                                item["type"] = "image"
                                data_list.append(item)
                            latest_db.insert_many(data_list)
                        return {"message": "uploaded succesfully"}, 200
                else:
                            
                    image_db[first][second].insert_one(data)  
                    image_db[first].find_one_and_update({"_id":second, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                    if latest == True:
                        latest_db.delete_many({"type":"image"})
                        data = image_db[first][second].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(5)
                        data_list = []
                        for item in data:
                            
                            item["type"] = "image"
                            data_list.append(item)
                        latest_db.insert_many(data_list)
                    return{"message":"uploaded successfully"}, 200
            else:
                
                image_db[first].insert_one(data)
                image_db.find_one_and_update({"_id":first, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                if latest == True:
                    latest_db.delete_many({"type":"image"})
                    data = image_db[first].find({"isFolder":False}).sort("timestamp", pymongo.DESCENDING).limit(5)
                    data_list = []
                    for item in data:
                        
                        item["type"] = "image"
                        data_list.append(item)
                    latest_db.insert_many(data_list)
                return {"message":"uploaded successfully"}, 200
        else:
            return {"message":"No Folder Specified"}, 400

    if request.method == "GET":
        page = request.args.get("page")
        skip_value = 30 * int(page)
        doc_list=[]
        if first != "_":
            if second != "_":
                if third != "_":
                    if fourth != "_":
                        if fifth != "_":
                            documents = image_db[first][second][third][fourth][fifth].find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                            for doc_ in documents :
                                doc_["id"] = doc_["_id"]
                                doc_.pop("_id")
                                doc_list.append(doc_)
                            return {"items":doc_list}, 200
                        else:
                            documents = image_db[first][second][third][fourth].find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                            for doc_ in documents :
                                doc_["id"] = doc_["_id"]
                                doc_.pop("_id")
                                doc_list.append(doc_)
                            return {"items":doc_list}, 200
                    else:
                        documents = image_db[first][second][third].find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                        for doc_ in documents :
                            doc_["id"] = doc_["_id"]
                            doc_.pop("_id")
                            doc_list.append(doc_)
                        return {"items":doc_list}, 200
                else:
                    documents = image_db[first][second].find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                    for doc_ in documents :
                        doc_["id"] = doc_["_id"]
                        doc_.pop("_id")
                        doc_list.append(doc_)
                    return {"items":doc_list}, 200
            else:
                documents = image_db[first].find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
                for doc_ in documents :
                    doc_["id"] = doc_["_id"]
                    doc_.pop("_id")
                    doc_list.append(doc_)
                return {"items":doc_list}, 200
        else:
            documents = image_db.find({"isFolder":False}).skip(skip_value).sort([("timestamp",pymongo.DESCENDING)]).limit(30)
            for doc_ in documents :
                doc_["id"] = doc_["_id"]
                doc_.pop("_id")
                doc_list.append(doc_)
            return {"items":doc_list}, 200

    if request.method == "PUT":
        info = request.json
        id  = info.get("id")
        latest = info.get("latest")
        keys = [i for i in info.keys()]
        data = {}
        for i in keys:
            if info.get(i) != "":
                data[i] = info.get(i)
        data.pop("id")
        data.pop("latest")
        doc_list = []
        try:
            if first != "_":
                if second != "_":
                    if third != "_":
                        if fourth != "_":
                            if fifth != "_":
                                image_db[first][second][third][fourth][fifth].find_one_and_update({"_id":id}, {"$set":data})
                                lis = image_db[first][second][third][fourth][fifth].find()
                                for lis_ in lis:
                                    lis_["id"] = lis_["_id"]
                                    lis_.pop("_id")
                                    doc_list.append(lis_)
                                if latest == True:
                                    if len(latest_image_items) == 5:
                                        latest_image_items.pop(0)
                                        latest_image_items.append(data)
                                    else:
                                        latest_image_items.append(data)
                                return {"message":"Document updated successfully", "images":doc_list}, 200
                            else:
                                image_db[first][second][third][fourth].find_one_and_update({"_id":id}, {"$set":data})
                                lis = image_db[first][second][third][fourth].find()
                                for lis_ in lis:
                                    lis_["id"] = lis_["_id"]
                                    lis_.pop("_id")
                                    doc_list.append(lis_)
                                if latest == True:
                                    if len(latest_image_items) == 5:
                                        latest_image_items.pop(0)
                                        latest_image_items.append(data)
                                    else:
                                        latest_image_items.append(data)
                                return {"message":"Document updated successfully", "images":doc_list}, 200
                        else:
                            image_db[first][second][third].find_one_and_update({"_id":id}, {"$set":data})
                            lis = image_db[first][second][third].find()
                            for lis_ in lis:
                                lis_["id"] = lis_["_id"]
                                lis_.pop("_id")
                                doc_list.append(lis_)
                            if latest == True:
                                    if len(latest_image_items) == 5:
                                        latest_image_items.pop(0)
                                        latest_image_items.append(data)
                                    else:
                                        latest_image_items.append(data)
                            return {"message":"Document updated successfully", "images":doc_list}, 200
                    else:
                        image_db[first][second].find_one_and_update({"_id":id}, {"$set":data})
                        lis = image_db[first][second].find()
                        for lis_ in lis:
                            lis_["id"] = lis_["_id"]
                            lis_.pop("_id")
                            doc_list.append(lis_)
                        if latest == True:
                                    if len(latest_image_items) == 5:
                                        latest_image_items.pop(0)
                                        latest_image_items.append(data)
                                    else:
                                        latest_image_items.append(data)
                        return {"message":"Document updated successfully", "images":doc_list}, 200
                else:
                    image_db[first].find_one_and_update({"_id":id}, {"$set":data})
                    lis = image_db[first].find()
                    for lis_ in lis:
                        lis_["id"] = lis_["_id"]
                        lis_.pop("_id")
                        doc_list.append(lis_)
                    if latest == True:
                                    if len(latest_image_items) == 5:
                                        latest_image_items.pop(0)
                                        latest_image_items.append(data)
                                    else:
                                        latest_image_items.append(data)
                    return {"message":"Document updated successfully", "images":doc_list}, 200
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
                            image_db[first][second][third][fourth].delete_one({"_id":id})
                            #audio_db[first][second][third][fourth][id].drop()
                            updated_folders = image_db[first][second][third][fourth].find({"isFolder":False})
                            for i in updated_folders:
                                folder_list.append(i)
                            return {"folders":folder_list}, 200
                    else:
                        image_db[first][second][third].delete_one({"_id":id})
                        #audio_db[first][second][third][id].drop()
                        updated_folders = image_db[first][second][third].find({"isFolder":False})
                        for i in updated_folders:
                            folder_list.append(i)
                        return {"folders":folder_list}, 200
                else:
                        image_db[first][second].delete_one({"_id":id})
                        #audio_db[first][second][id].drop()
                        updated_folders = image_db[first][second].find({"isFolder":False})
                        for i in updated_folders:
                            folder_list.append(i)
                        return {"folders":folder_list}, 200
            else:
                image_db[first].delete_one({"_id":id})
                #audio_db[first][id].drop()
                updated_folders = image_db[first].find({"isFolder":False})
                for i in updated_folders:
                    folder_list.append(i)
                return {"folders":folder_list}, 200
        else:
            image_db.delete_one({"_id":id})
            #audio_db[id].drop()
            updated_folders = image_db.find({"isFolder":False})
            for i in updated_folders:
                folder_list.append(i)
            return {"folders":folder_list}, 200
   

@image.route("Items_batch/<first>/<second>/<third>/<fourth>/<fifth>", methods=["POST"])
def batch(first, second, third, fourth, fifth):
    if request.method == "POST":
        images = request.json.get("images")
        #image_db.insert_many(images)
        #return {"message":"Documents Uploaded"}, 200
        for i in images:
            i["_id"] = i["id"]
            i["isFolder"] = False
            i.pop("id")
            if i["latest"] == True:
                if len(latest_image_items) == 5:
                    i.pop("latest")
                    latest_image_items.pop(0)
                    latest_image_items.append(i)
                else:
                    i.pop("latest")
                    latest_image_items.append(i)
            else: i.pop("latest")
        #print(latest_image_items)
        if first!= "_":
            if second != "_" :
                if third != "_" :
                    if fourth != "_":
                        if fifth != "_":
                            image_db[first][second][third][fourth][fifth].insert_many(images)
                            image_db[first][second][third][fourth].find_one_and_update({"_id":fifth, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                            
                            return {"message":"uploaded successfuly"}, 200

                        else:
                            image_db[first][second][third][fourth].insert_many(images)
                            image_db[first][second][third].find_one_and_update({"_id":fourth, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                            
                            return {"message":"uploaded successfully"},200
                    else:
                            
                        image_db[first][second][third].insert_many(images)
                        image_db[first][second].find_one_and_update({"_id":third, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                        
                        return {"message": "uploaded succesfully"}, 200
                else:
                            
                    image_db[first][second].insert_many(images)  
                    image_db[first].find_one_and_update({"_id":second, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                    
                    return{"message":"uploaded successfully"}, 200
            else:
                
                image_db[first].insert_many(images)
                image_db.find_one_and_update({"_id":first, "isFolder":True}, {"$set":{"is_finalFolder":True}})
                
                return {"message":"uploaded successfully"}, 200
        else:
            return {"message":"No Folder Specified"}, 400