import os
from dotenv import load_dotenv
import requests
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Load .env
dotenv_path = r"D:\ai-health-chatbot\backend\.env"
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(f".env file not found at {dotenv_path}")
load_dotenv(dotenv_path)

# Safely get environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")
RASA_BASE_URL = os.getenv("RASA_BASE_URL")

# DEBUG: check if variables are loaded
print("MONGO_URI:", MONGO_URI)
print("MONGO_DB:", MONGO_DB)
print("OPENAI_API_KEY:", (OPENAI_API_KEY[:10] + "...") if OPENAI_API_KEY else None)
print("GEMINI_API_KEY:", (GEMINI_API_KEY[:10] + "...") if GEMINI_API_KEY else None)
print("HF_API_KEY:", (HF_API_KEY[:10] + "...") if HF_API_KEY else None)
print("RASA_BASE_URL:", RASA_BASE_URL)

# 1️⃣ MongoDB Test
async def test_mongo():
    if not MONGO_URI or not MONGO_DB:
        print("❌ MongoDB Error: MONGO_URI or MONGO_DB not set")
        return
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[MONGO_DB]
        collections = await db.list_collection_names()
        print(f"✅ MongoDB Connected. Collections: {collections}")
    except Exception as e:
        print(f"❌ MongoDB Error: {e}")

# 2️⃣ Rasa Test
def test_rasa():
    if not RASA_BASE_URL:
        print("❌ Rasa Error: RASA_BASE_URL not set")
        return
    try:
        url = f"{RASA_BASE_URL}/status"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            print(f"✅ Rasa Server OK: {res.json()}")
        else:
            print(f"❌ Rasa Error: Status {res.status_code}")
    except Exception as e:
        print(f"❌ Rasa Connection Error: {e}")

# 3️⃣ OpenAI Test
def test_openai():
    if not OPENAI_API_KEY:
        print("❌ OpenAI Error: OPENAI_API_KEY not set")
        return
    try:
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        res = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=5)
        if res.status_code == 200:
            print(f"✅ OpenAI Key Works. Models count: {len(res.json().get('data', []))}")
        else:
            print(f"❌ OpenAI Error: {res.status_code} {res.text}")
    except Exception as e:
        print(f"❌ OpenAI Connection Error: {e}")

# Run all tests
async def main():
    await test_mongo()
    test_rasa()
    test_openai()

if __name__ == "__main__":
    asyncio.run(main())
