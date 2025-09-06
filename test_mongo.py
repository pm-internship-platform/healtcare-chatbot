from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot"]
users = db["users"]

result = users.insert_one({"name": "TestUser"})
print("✅ Inserted ID:", result.inserted_id)

print("All docs in collection:")
for doc in users.find():
    print(doc)
