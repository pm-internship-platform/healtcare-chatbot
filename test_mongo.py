from pymongo import MongoClient

client = MongoClient("mongodb+srv://samjoshua:jRbkfyiBv4x9BNc3@cluster0.ztkza3f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["health_chatbot"]
users = db["hackathon"]

result = users.insert_one({"name": "TestUser"})
print("✅ Inserted ID:", result.inserted_id)

print("All docs in collection:")
for doc in users.find():
    print(doc)
