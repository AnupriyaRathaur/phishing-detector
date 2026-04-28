from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["phishing_db"]
collection = db["predictions"]

def save_result(data):
    try:
        collection.insert_one(data)
        print("✅ Saved to DB")
    except Exception as e:
        print("❌ DB Error:", e)