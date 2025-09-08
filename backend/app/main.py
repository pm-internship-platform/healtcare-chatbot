# D:\ultra-chatbot\backend\app\main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.app.services.disease_service import predict_disease  # ✅ Correct import

app = FastAPI(title="Ultra-Chatbot Disease Prediction API")

class SymptomInput(BaseModel):
    features: dict  # e.g., {"symptom1": 0, "symptom2": 1, ...}

@app.get("/")
def root():
    return {"message": "Ultra-Chatbot API is running"}

@app.post("/predict")
def predict(input_data: SymptomInput, model_type: str = "rf"):
    """
    model_type: "rf" for Random Forest, "nn" for Neural Network
    """
    try:
        disease = predict_disease(input_data.features, model_type)
        return {"disease": disease}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
