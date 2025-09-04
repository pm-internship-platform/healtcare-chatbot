import httpx
import os

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    async def chat(self, message: str) -> str:
        if not self.api_key:
            return "OpenAI API key not configured."

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7
        }

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, headers=headers, json=payload)
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
