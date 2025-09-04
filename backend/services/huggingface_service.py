import os
import httpx

class HuggingFaceService:
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        self.base_url = "https://api-inference.huggingface.co/models"

    async def chat(self, message: str, model: str = "gpt2") -> str:
        if not self.api_key:
            return "HuggingFace API key not configured."

        url = f"{self.base_url}/{model}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"inputs": message, "options": {"wait_for_model": True}}

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, headers=headers, json=payload)
            data = resp.json()
            if isinstance(data, list) and data and "generated_text" in data[0]:
                return data[0]["generated_text"]
            return str(data)
