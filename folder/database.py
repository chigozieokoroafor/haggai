import pymongo


#client = pymongo.MongoClient("mongodb+srv://haggai:haggai@cluster0.jv2up.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

client = pymongo.MongoClient("mongodb://localhost:27017")

database = client.haggai_database
daily_verse_db = database.daily_verse
devotion_list_db = database["devotions"]
live_videos_db = database["live_videos"]
mixlir_db =  database.mixlir
audio_db = database["audio"]
videos_db = database["videos"]
theme_db = database["themes"]
sermon_db = database["sermon_notes"]
image_db = database["images"]
latest_db = database["latest"]
devotion_types = database.devotion_types
