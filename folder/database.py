import pymongo

client = pymongo.MongoClient(connectionString)
database = client.haggai_database
daily_verse_db = database.daily_verse
devotion_list_db = database.devotions.RCCG
live_videos_db = database.live_videos
mixlir_db =  database.mixlir
audio_db = database["audio"]
theme_db = database.themes
sermon_db = database["sermon_notes"]
image_db = database["images"]
latest_db = database["latest"]
