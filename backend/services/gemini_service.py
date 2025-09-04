import httpx
import os

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

    async def chat(self, message: str) -> str:
        if not self.api_key:
            return "Gemini API key not configured."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": message}]}]
        }

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=payload)
            data = resp.json()
            return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No reply")
