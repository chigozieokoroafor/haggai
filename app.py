import pymongo 
from flask import Flask, request,Response, jsonify
from flask_cors import CORS
from datetime import datetime
from bson import ObjectId



app = Flask(__name__)
CORS(app)


client = pymongo.MongoClient("mongodb+srv://haggai:haggai@cluster0.jv2up.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client.haggai_database


def check_for_zero(x):
    num = []
    x = int(x)
    if x<10:
        for i in str(x):
            number = int(i)
            num.append(number)
        if num[0]!=0:return '0'+ str(x)
        else: return x       
    else: return x

def check_date(datetime_):
    today = datetime.today().date()
    d_ = datetime.strptime(datetime_, "%Y-%m-%d %H:%M:%S")
    date = d_.date()
    check = today > date
    return check


date = datetime.now()
date_ = date.strftime("%Y-%m-%d %H:%M:%S" )


@app.route("/home/today_bible_verse", methods=["GET", "POST"])
def bible_verse():
    daily_verse = database.daily_verse
    if request.method == "GET":
        try:
            verse = daily_verse.find_one({"day": str(check_for_zero(date.day)),
                                                #"year": str(check_for_zero(date.year)),
                                                "month": str(check_for_zero(date.month))})
            
            return ({"verse_of_the_day":verse["verse_body"], 
                         "verse_title":verse["verse_title"],
                         "date_uploaded":verse["date_uploaded"],
                         "type":"success"}, 200)

            
        except TypeError:
            return ({"message":"No verse for the day", "type":"fail"}, 400)

    if request.method == "POST":
        verse_title = request.json.get("verse_title")
        verse_body = request.json.get("verse_body")
        day_to_be_shown = request.json.get("day_to_be_shown")
        month_to_be_shown = request.json.get("month_to_be_shown")
        date_uploaded = date_
        img_url = request.json.get("image_url")

        daily_verse.insert_one({
                                "verse_title":verse_title,
                                "verse_body":verse_body,
                                "day":day_to_be_shown,
                                "month":month_to_be_shown,
                                "date_uploaded":date_uploaded,
                                "image_url": img_url
                                })
        
        return ({"message":"just uploaded successfully", "type":"static"}, 200)


@app.route("/home/devotions", methods=["GET", "POST"])
def home_devotions():
    
    devotion_list = database.devotions.RCCG
    L =[]
    if request.method == "GET":
        try:
            dev_id = request.args["devotion_id"]
            dev_list = dev_id.split(", ")
            #print(dev_list)
            if len(dev_list)>1:
                for _id in dev_list:
                    devotion = devotion_list.find_one({"id":_id})
                    L.append({"Devotion Name": devotion["name"],
                            "Devotion Description":devotion["description"],
                            "Devotion Type": devotion["type"]})
                
                return ({"items":L, "type":"success"}, 200)
            
            elif len(dev_list)==1:
                devotion = devotion_list.find_one({"id":dev_id})
                return ({"Devotion Name": devotion["name"],
                        "Devotion Description":devotion["description"],
                        "Devotion Type": devotion["type"],
                        "type":"success"}, 200)  
        except:
            return ({"message":"no devotion_id provided", "type":"error"}, 400) 
        


    if request.method == "POST":
        return ({"message":"work in progress", "type":"static"}, 204)


#there should be a maximum of 5 videos in this Db
@app.route("/home/live_videos", methods= ["GET", "PUT"])
def live_video():
    videos = database.live_videos
    
    if request.method == "GET":
        v = videos.find()
        v_list = []
        for v_ in v:
            v_list.append({"live_video_url":v_["url"],
                    "live_video_name":v_["name"],
                    "isLive":True})
        return {"items":v_list}, 200
        
    if request.method == "PUT":
        try:
            url=  request.json.get("video_url")
            name = request.json.get("video_name")
            isLive = request.json.get("isLive")
            

            if url==None or name==None or isLive==None:
                return ({"message":"nothing was provided"}, 400)

            else:
                for video_info in videos.find():
                    if check_date(video_info["datetime"]) == True:
                        videos.find_one_and_delete(video_info)
                            
                if videos.count_documents({})<5:
                    item = {"name":name, "url":url, "datetime":date_, "isLive":isLive}
                    videos.insert_one(item)
                    return({"message":"added successfully"}, 200)
                else:
                    return ({"message":"maximum items reached"}, 400)
                        
            

        except AttributeError:
            return {"message":"Something went wrong"}, 400


# there is only one item in the mixlir database
@app.route("/home/live_mixlir", methods=["GET", "POST", "PUT"])
def home_mixlir():
    mixlir_db =  database.mixlir
    item = mixlir_db.find_one()

    if request.method == "GET":
        return {"url": item["url"], "name": item["name"], "date_uploaded":item["date_uploaded"]}, 200

    if request.method == "POST":
        mixlir = request.json
        url = mixlir.get("mixlir_url")
        name = mixlir.get("mixlir_name")
        mixlir_db.insert_one({"url":url,
                              "name":name,
                              "date_uploaded": date_})
        return({"message":(url, name)}, 200)

    if request.method == "PUT":
        mixlir = request.json
        url = mixlir.get("mixlir_url")
        name = mixlir.get("mixlir_name")
        mixlir_db.find_one_and_update({"_id":ObjectId(item["_id"])},
                                      {"$set":{"url":url,
                                               "name":name,
                                               "date_updated": date_}})
        return({"message":"updated successfully"}, 200)


#for the devotions Screen 
@app.route("/devotions", methods=["GET", "POST"])
def devotion():
    if request.method == "GET":

    
        return("work in progress", 200)


#for the themes 
@app.route("/themes", methods=["POST", "GET"])
def themes():
    theme = database.themes
    if request.method == "GET":
        theme_list_ = []
        theme_list = theme.find().sort("rank", -1)
        for theme_ in theme_list:
            theme_list_.append({"name":theme_["theme_name"],
                                "dark_image_url":theme_["dark_image_url"],
                                "light_image_url":theme_["light_image_url"],
                                "rank":theme_["rank"]})
        
        return ({"items":theme_list_}, 200)
        
    if request.method == "POST":
        theme_ = request.json
        theme_url_light = theme_.get("light_url")
        theme_url_dark = theme_.get("dark_url")
        theme_name = theme_.get("name")
        theme_rank = theme_.get("Rank")
        date_uploaded = date_
        theme.insert_one({"light_image_url":theme_url_light,
                          "dark_image_url":theme_url_dark,
                          "theme_name":theme_name,
                          "rank":theme_rank,
                          "date_uploaded":date_uploaded})

        return ({"message":"work in progress", "type":"static"}, 204)

if __name__=="__main__":
    app.run(debug=True)