import pymongo 
from flask import Flask, request
from flask_cors import CORS
from datetime import datetime

from sqlalchemy import null

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
            
date = datetime.utcnow()


@app.route("/home/today_bible_verse", methods=["GET", "POST"])
def bible_verse():
    if request.method == "GET":
        daily_verse = database.daily_verse
        try:
            verse = daily_verse.find_one({"day": check_for_zero(str(date.day)),
                                                "year": check_for_zero(str(date.year)),
                                                "month": check_for_zero(str(date.month))})
            
            return ({"verse_of the day":verse["verse_body"], 
                         "verse_title":verse["verse_title"]})

            
        except TypeError:
            return "No verse for the day "

    if request.method == "POST":
        dev = request.form.get("dev")
        
        return("work in progress")


@app.route("/home/devotions", methods=["POST", "GET"])
def devotions():
    if request.method == "GET":
        dev_id = request.args.get("devotion_id")
        dev_id = [dev_id]
        devotion_ = database.devotions.RCCG
        devotion = devotion_.find_one({"id":dev_id})
        #l = []
        for i in database.list_collections():
            x = database[i["name"]].find_one({"parent_id": devotion["id"],     
                                        "day": check_for_zero(str(date.day)),
                                        "year": check_for_zero(str(date.year)),
                                        "month": check_for_zero(str(date.month))})
            if x!= None: 
               return ({"devotion":devotion["name"],
                        "devotion description":devotion["description"],
                        "title":x["title"],
                        "items":x["mdevotionItems"],
                        "audio_url":x["audio_url"],
                         "image_url":x["image_url"],
                          "page_url":x["page_url"]}, 200)
            

        return ({"message":"no devotion for today"}, 205)

    if request.method == "POST":
        dev = request.form.get("")


@app.route("/themes", methods=["POST", "GET"])
def themes():
    theme = database.theme
    if request.method == "GET":
        pass
        
    if request.method == "POST":
        pass

if __name__=="__main__":
    app.run(debug=True)