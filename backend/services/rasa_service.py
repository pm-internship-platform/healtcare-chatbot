import os
import httpx

class RasaService:
    def __init__(self):
        self.base_url = os.getenv("RASA_BASE_URL", "http://localhost:5005")

    async def chat(self, user_id: str = "user", message: str = "") -> str:
        url = f"{self.base_url.rstrip('/')}/webhooks/rest/webhook"
        payload = {"sender": user_id, "message": message}

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=payload)
            data = resp.json()
            replies = [d.get("text", "") for d in data if isinstance(d, dict)]
            return "\n".join(replies) if replies else "No reply from Rasa"
