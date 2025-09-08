from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import os

API_URL = os.getenv("ULTRA_CHATBOT_API", "http://localhost:8000/predict")

class ActionPredictDisease(Action):
    def name(self):
        return "action_predict_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain):
        
        # Example: collect symptoms from slots
        symptoms = {}
        for slot_name in tracker.slots:
            symptoms[slot_name] = tracker.get_slot(slot_name) or 0
        
        response = requests.post(API_URL, json={"features": symptoms, "model_type": "rf"})
        disease = response.json().get("disease", "Unknown")
        
        dispatcher.utter_message(text=f"Based on the symptoms, the predicted disease is: {disease}")
        return []
