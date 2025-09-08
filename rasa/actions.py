# rasa/actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ActionHealthResponse(Action):
    def name(self) -> Text:
        return "action_health_response"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the user message
        user_message = tracker.latest_message.get('text')
        
        # Call the backend API
        try:
            response = requests.post(
                "http://localhost:8000/api/chat",
                json={
                    "message": user_message,
                    "user_id": tracker.sender_id,
                    "language": "en"  # Default, can be extended
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                dispatcher.utter_message(text=data['response'])
            else:
                dispatcher.utter_message(text="I'm having trouble connecting to the health service. Please try again later.")
                
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I encountered an error. Please try again.")
            
        return []

class ActionProvideDiseaseInfo(Action):
    def name(self) -> Text:
        return "action_provide_disease_info"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        disease = tracker.get_slot('disease')
        if not disease:
            dispatcher.utter_message(text="Which disease would you like information about?")
            return []
        
        try:
            response = requests.get(
                f"http://localhost:8000/api/health/disease-info/{disease}",
                params={"language": "en"}
            )
            
            if response.status_code == 200:
                data = response.json()
                message = f"Information about {disease}:\n\n"
                message += f"Symptoms: {data.get('symptoms', 'Not available')}\n\n"
                message += f"Prevention: {data.get('prevention', 'Not available')}\n\n"
                message += f"Treatment: {data.get('treatment', 'Not available')}"
                
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find information about {disease}.")
                
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I encountered an error. Please try again.")
            
        return []

class ActionProvideVaccinationInfo(Action):
    def name(self) -> Text:
        return "action_provide_vaccination_info"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Default to child vaccination schedule
        age = tracker.get_slot('age') or 5
        
        try:
            response = requests.get(
                "http://localhost:8000/api/health/vaccination-schedule",
                params={"age": age, "language": "en"}
            )
            
            if response.status_code == 200:
                data = response.json()
                dispatcher.utter_message(text=data)
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve the vaccination schedule.")
                
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I encountered an error. Please try again.")
            
        return []

class ActionProvideHealthAlerts(Action):
    def name(self) -> Text:
        return "action_provide_health_alerts"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        district = tracker.get_slot('district') or "Bhubaneswar"
        
        try:
            response = requests.get(
                f"http://localhost:8000/api/health/outbreak-alerts/{district}",
                params={"language": "en"}
            )
            
            if response.status_code == 200:
                data = response.json()
                alerts = data.get('alerts', [])
                
                if alerts:
                    message = f"Health alerts for {district}:\n\n"
                    for alert in alerts:
                        message += f"• {alert}\n"
                    dispatcher.utter_message(text=message)
                else:
                    dispatcher.utter_message(text=f"No current health alerts for {district}.")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't retrieve health alerts.")
                
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I encountered an error. Please try again.")
            
        return []

class ActionStartQuiz(Action):
    def name(self) -> Text:
        return "action_start_quiz"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="I'll start a health quiz for you! Please use the quiz button in the chat interface to begin.")
        return []