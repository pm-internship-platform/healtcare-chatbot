from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
import re

# Emergency symptoms that require immediate medical attention
EMERGENCY_SYMPTOMS = [
    "chest pain", "difficulty breathing", "shortness of breath", "severe bleeding",
    "stroke symptoms", "heart attack", "severe burns", "unconscious", "seizure",
    "severe allergic reaction", "choking", "severe head injury", "severe trauma",
    "can't breathe", "severe abdominal pain", "severe mental health crisis"
]

# Comprehensive symptom database with advice
SYMPTOM_DATABASE = {
    "headache": {
        "mild": "Rest in a quiet, dark room. Stay hydrated and consider over-the-counter pain relief.",
        "moderate": "Rest, hydrate, and take pain medication as directed. If persistent, monitor closely.",
        "severe": "Seek medical attention if severe headache persists or is accompanied by fever, stiff neck, or vision changes."
    },
    "migraine": {
        "mild": "Rest in a dark, quiet room. Apply cold compress to forehead. Stay hydrated.",
        "moderate": "Take prescribed migraine medication early. Rest in dark room. Avoid triggers.",
        "severe": "Take prescribed medication immediately. If no relief in 2 hours, consider medical attention."
    },
    "fever": {
        "mild": "Rest, stay hydrated, monitor temperature. Use fever reducers as needed.",
        "moderate": "Rest, increase fluid intake, use fever-reducing medication, monitor symptoms.",
        "severe": "Seek medical attention if fever exceeds 103°F (39.4°C) or persists more than 3 days."
    },
    "cough": {
        "mild": "Stay hydrated, use throat lozenges, consider honey for soothing.",
        "moderate": "Rest, warm liquids, humidifier, over-the-counter cough suppressants.",
        "severe": "If cough persists more than 3 weeks or produces blood, seek medical attention."
    },
    "sore throat": {
        "mild": "Gargle with warm salt water, stay hydrated, throat lozenges.",
        "moderate": "Rest, warm liquids, pain relievers, salt water gargles.",
        "severe": "If accompanied by high fever or difficulty swallowing, see a doctor."
    },
    "stomach ache": {
        "mild": "Rest, stay hydrated, BRAT diet (bananas, rice, applesauce, toast).",
        "moderate": "Clear liquids, rest, avoid solid foods until symptoms improve.",
        "severe": "Seek medical attention if severe pain, vomiting, or signs of dehydration."
    },
    "back pain": {
        "mild": "Rest, gentle stretching, heat/cold therapy, over-the-counter pain relief.",
        "moderate": "Balance rest with gentle movement, pain medication, consider physical therapy.",
        "severe": "Medical evaluation needed, especially if pain radiates to legs or causes numbness."
    },
    "joint pain": {
        "mild": "Rest affected joint, apply ice/heat, gentle movement, over-the-counter anti-inflammatory.",
        "moderate": "Balance rest and gentle exercise, consider anti-inflammatory medication.",
        "severe": "Medical evaluation needed, especially if joint is swollen or warm."
    },
    "fatigue": {
        "mild": "Ensure adequate sleep, balanced diet, regular exercise, manage stress.",
        "moderate": "Prioritize rest, evaluate sleep quality, consider vitamin deficiencies.",
        "severe": "If persistent fatigue affects daily activities, medical evaluation recommended."
    },
    "dizziness": {
        "mild": "Sit or lie down, stay hydrated, move slowly when changing positions.",
        "moderate": "Rest, hydrate, avoid sudden movements, monitor for improvement.",
        "severe": "Seek medical attention if accompanied by chest pain, shortness of breath, or confusion."
    },
    "nausea": {
        "mild": "Stay hydrated with small sips, try ginger, eat bland foods.",
        "moderate": "Clear liquids, rest, avoid strong odors, small frequent meals.",
        "severe": "If persistent vomiting or signs of dehydration, seek medical attention."
    },
    "anxiety": {
        "mild": "Practice deep breathing, mindfulness, regular exercise, limit caffeine.",
        "moderate": "Consider relaxation techniques, talk to someone you trust, maintain routine.",
        "severe": "If anxiety interferes with daily life, consider professional mental health support."
    },
    "depression": {
        "mild": "Maintain social connections, regular exercise, good sleep hygiene, engage in activities you enjoy.",
        "moderate": "Reach out to friends/family, consider counseling, maintain healthy habits.",
        "severe": "Professional mental health support recommended. If thoughts of self-harm, seek immediate help."
    }
}

# Prevention tips for common symptoms
PREVENTION_TIPS = {
    "headache": "Stay hydrated, maintain regular sleep schedule, manage stress, avoid known triggers.",
    "migraine": "Identify and avoid triggers, maintain consistent sleep schedule, manage stress, stay hydrated.",
    "fever": "Good hand hygiene, avoid contact with sick individuals, maintain strong immune system.",
    "cough": "Avoid irritants, don't smoke, wash hands frequently, stay hydrated.",
    "sore throat": "Good hand hygiene, avoid close contact with sick people, don't share utensils.",
    "stomach ache": "Eat slowly, avoid trigger foods, manage stress, maintain good food hygiene.",
    "back pain": "Good posture, regular exercise, proper lifting techniques, ergonomic workspace.",
    "joint pain": "Regular exercise, maintain healthy weight, protect joints during activities.",
    "fatigue": "Regular sleep schedule, balanced diet, regular exercise, stress management.",
    "anxiety": "Regular exercise, stress management techniques, limit caffeine, maintain social connections.",
    "depression": "Regular exercise, social connections, adequate sleep, engage in meaningful activities."
}

class ActionProvideHealthAdvice(Action):
    def name(self) -> Text:
        return "action_provide_health_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptom = tracker.get_slot("symptom")
        duration = tracker.get_slot("duration")
        severity = tracker.get_slot("severity")
        age = tracker.get_slot("age")
        
        if not symptom:
            dispatcher.utter_message(text="I need to know your symptoms to provide appropriate advice. What are you experiencing?")
            return []
        
        # Check for emergency symptoms first
        if any(emergency in symptom.lower() for emergency in EMERGENCY_SYMPTOMS):
            dispatcher.utter_message(text="🚨 **EMERGENCY ALERT** 🚨\n\nBased on your symptoms, you need IMMEDIATE medical attention!\n\n📞 Call Emergency Services NOW:\n• USA: 911\n• UK: 999\n• Europe: 112\n\n🏥 Go to the nearest Emergency Room immediately!")
            return []
        
        # Normalize symptom for lookup
        normalized_symptom = symptom.lower().strip()
        
        # Get advice based on symptom and severity
        advice = self.get_symptom_advice(normalized_symptom, severity)
        
        # Build comprehensive response
        response = f"**Health Assessment for: {symptom.title()}**\n\n"
        
        if duration:
            response += f"⏱️ **Duration:** {duration}\n"
        if severity:
            response += f"📊 **Severity:** {severity}\n"
        if age:
            response += f"👤 **Age:** {age}\n"
        
        response += f"\n💡 **Recommendation:**\n{advice}\n"
        
        # Add duration-based advice
        if duration:
            duration_advice = self.get_duration_advice(duration, normalized_symptom)
            if duration_advice:
                response += f"\n⏰ **Duration Consideration:** {duration_advice}\n"
        
        # Add age-specific advice
        if age:
            age_advice = self.get_age_advice(age, normalized_symptom)
            if age_advice:
                response += f"\n👨‍⚕️ **Age Consideration:** {age_advice}\n"
        
        # Add when to seek medical attention
        when_to_seek = self.get_when_to_seek_help(normalized_symptom, severity, duration)
        if when_to_seek:
            response += f"\n🏥 **Seek Medical Attention If:** {when_to_seek}\n"
        
        response += "\n⚠️ **Important:** This is general information only and not a substitute for professional medical advice."
        
        dispatcher.utter_message(text=response)
        
        return []

    def get_symptom_advice(self, symptom: str, severity: str) -> str:
        """Get advice based on symptom and severity"""
        
        # Check if symptom exists in database
        for key in SYMPTOM_DATABASE:
            if key in symptom or symptom in key:
                severity_level = "mild"
                if severity:
                    if any(word in severity.lower() for word in ["severe", "unbearable", "intense"]):
                        severity_level = "severe"
                    elif any(word in severity.lower() for word in ["moderate", "medium"]):
                        severity_level = "moderate"
                
                return SYMPTOM_DATABASE[key].get(severity_level, SYMPTOM_DATABASE[key]["mild"])
        
        # Generic advice for unknown symptoms
        if severity and any(word in severity.lower() for word in ["severe", "unbearable", "intense"]):
            return "For severe symptoms, it's recommended to seek medical attention promptly."
        else:
            return "Monitor your symptoms, rest, stay hydrated, and consider over-the-counter remedies as appropriate."

    def get_duration_advice(self, duration: str, symptom: str) -> str:
        """Provide advice based on symptom duration"""
        
        duration_lower = duration.lower()
        
        if any(word in duration_lower for word in ["weeks", "months", "chronic", "long"]):
            return "Chronic symptoms warrant medical evaluation to rule out underlying conditions."
        elif any(word in duration_lower for word in ["days", "week"]):
            return "Symptoms lasting several days should be monitored closely."
        elif any(word in duration_lower for word in ["hours", "today", "just started"]):
            return "For new symptoms, monitor closely and seek care if they worsen."
        
        return ""

    def get_age_advice(self, age: str, symptom: str) -> str:
        """Provide age-specific advice"""
        
        try:
            age_num = int(re.search(r'\d+', age).group())
            
            if age_num < 18:
                return "For children and adolescents, consider consulting with a pediatrician."
            elif age_num > 65:
                return "Older adults should be more cautious with symptoms and consider earlier medical consultation."
            elif age_num > 50:
                return "Consider age-related health factors and don't hesitate to seek medical advice."
        except:
            pass
        
        return ""

    def get_when_to_seek_help(self, symptom: str, severity: str, duration: str) -> str:
        """Provide guidance on when to seek medical help"""
        
        general_warnings = [
            "Symptoms worsen or don't improve",
            "You develop additional concerning symptoms",
            "You have difficulty with daily activities",
            "You're concerned about your symptoms"
        ]
        
        symptom_specific = {
            "headache": ["sudden severe headache", "headache with fever and stiff neck", "headache with vision changes"],
            "fever": ["fever above 103°F (39.4°C)", "fever with severe headache", "fever with difficulty breathing"],
            "chest pain": ["any chest pain", "pain radiating to arm or jaw", "chest pain with shortness of breath"],
            "abdominal pain": ["severe abdominal pain", "pain with vomiting blood", "signs of dehydration"],
            "back pain": ["pain radiating to legs", "numbness or weakness", "loss of bladder control"]
        }
        
        warnings = general_warnings.copy()
        
        for key, specific_warnings in symptom_specific.items():
            if key in symptom:
                warnings.extend(specific_warnings)
                break
        
        return "; ".join(warnings)


class ActionAssessEmergency(Action):
    def name(self) -> Text:
        return "action_assess_emergency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptom = tracker.get_slot("symptom") or ""
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Check for emergency keywords
        emergency_detected = False
        
        for emergency_symptom in EMERGENCY_SYMPTOMS:
            if emergency_symptom in symptom.lower() or emergency_symptom in user_message:
                emergency_detected = True
                break
        
        # Additional emergency indicators
        emergency_indicators = [
            "can't breathe", "difficulty breathing", "chest pain", "severe pain",
            "heart attack", "stroke", "unconscious", "bleeding heavily",
            "severe burns", "poisoning", "overdose", "suicide", "self harm"
        ]
        
        for indicator in emergency_indicators:
            if indicator in user_message:
                emergency_detected = True
                break
        
        if emergency_detected:
            return [SlotSet("emergency_detected", True)]
        
        return [SlotSet("emergency_detected", False)]


class ActionProvidePreventionTips(Action):
    def name(self) -> Text:
        return "action_provide_prevention_tips"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptom = tracker.get_slot("symptom")
        
        response = "🛡️ **Health Prevention Tips:**\n\n"
        
        if symptom:
            # Get specific prevention tip
            normalized_symptom = symptom.lower().strip()
            prevention_tip = None
            
            for key in PREVENTION_TIPS:
                if key in normalized_symptom or normalized_symptom in key:
                    prevention_tip = PREVENTION_TIPS[key]
                    break
            
            if prevention_tip:
                response += f"**For {symptom.title()}:**\n{prevention_tip}\n\n"
        
        # General health tips
        response += """**General Health Prevention:**
• 🥗 Maintain a balanced diet rich in fruits and vegetables
• 💧 Stay well hydrated (8+ glasses of water daily)
• 🏃‍♂️ Exercise regularly (at least 30 minutes, 5 days a week)
• 😴 Get adequate sleep (7-9 hours per night)
• 🧼 Practice good hygiene (frequent hand washing)
• 🚭 Avoid smoking and limit alcohol consumption
• 🧘‍♀️ Manage stress through relaxation techniques
• 💉 Keep up with regular medical checkups and vaccinations
• 🏥 Know when to seek medical attention
• 👥 Maintain healthy social connections"""
        
        dispatcher.utter_message(text=response)
        
        return []


class ActionSuggestNextSteps(Action):
    def name(self) -> Text:
        return "action_suggest_next_steps"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptom = tracker.get_slot("symptom")
        severity = tracker.get_slot("severity")
        duration = tracker.get_slot("duration")
        
        response = "📋 **Recommended Next Steps:**\n\n"
        
        # Determine urgency level
        urgency = self.assess_urgency(symptom, severity, duration)
        
        if urgency == "high":
            response += """🚨 **High Priority - Seek Medical Attention:**
• Contact your doctor today or visit urgent care
• Consider emergency room if symptoms are severe
• Don't wait if symptoms worsen
• Have someone accompany you if possible"""
        
        elif urgency == "medium":
            response += """⚠️ **Medium Priority - Monitor and Schedule:**
• Schedule appointment with your primary care doctor within a few days
• Continue monitoring symptoms
• Keep a symptom diary
• Seek immediate care if symptoms worsen"""
        
        else:  # low urgency
            response += """✅ **Low Priority - Self-Care and Monitor:**
• Continue self-care measures
• Monitor symptoms for changes
• Consider seeing a doctor if symptoms persist beyond a week
• Schedule routine checkup if due"""
        
        response += "\n\n**General Recommendations:**\n"
        response += "• 📝 Keep a symptom diary with dates, times, and descriptions\n"
        response += "• 💊 Follow medication instructions carefully\n"
        response += "• 🏠 Create a comfortable recovery environment\n"
        response += "• 👥 Inform trusted contacts about your condition\n"
        response += "• 📞 Keep emergency numbers readily available"
        
        dispatcher.utter_message(text=response)
        
        return []
    
    def assess_urgency(self, symptom: str, severity: str, duration: str) -> str:
        """Assess urgency level based on symptoms"""
        
        if not symptom:
            return "low"
        
        symptom_lower = symptom.lower()
        
        # High urgency symptoms
        high_urgency = [
            "chest pain", "difficulty breathing", "severe bleeding", "severe burns",
            "head injury", "stroke symptoms", "heart attack", "severe allergic reaction"
        ]
        
        for high_symptom in high_urgency:
            if high_symptom in symptom_lower:
                return "high"
        
        # Check severity
        if severity and any(word in severity.lower() for word in ["severe", "unbearable", "intense"]):
            return "high"
        
        # Check duration
        if duration and any(word in duration.lower() for word in ["weeks", "months", "chronic"]):
            return "medium"
        
        # Medium urgency symptoms
        medium_urgency = [
            "persistent fever", "severe headache", "abdominal pain", "joint swelling",
            "vision problems", "hearing loss", "persistent cough"
        ]
        
        for medium_symptom in medium_urgency:
            if medium_symptom in symptom_lower:
                return "medium"
        
        return "low"


class ValidateSymptomForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_symptom_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["symptom", "duration", "severity"]

    def validate_symptom(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        if slot_value and len(slot_value.strip()) > 2:
            return {"symptom": slot_value}
        else:
            dispatcher.utter_message(text="Please describe your symptom in more detail.")
            return {"symptom": None}

    def validate_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        if slot_value:
            return {"duration": slot_value}
        else:
            dispatcher.utter_message(text="Please let me know how long you've had this symptom.")
            return {"duration": None}

    def validate_severity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        if slot_value:
            return {"severity": slot_value}
        else:
            dispatcher.utter_message(text="Please rate the severity of your symptom (mild, moderate, or severe).")
            return {"severity": None}


class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [AllSlotsReset()]