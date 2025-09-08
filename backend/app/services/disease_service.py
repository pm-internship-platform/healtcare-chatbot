import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import os

# Base path of this file
BASE_DIR = os.path.dirname(__file__)

# Load models with absolute paths
rf_model = joblib.load(os.path.join(BASE_DIR, "../models/disease_rf_model.pkl"))
nn_model = load_model(os.path.join(BASE_DIR, "../models/disease_nn_model.h5"))
scaler = joblib.load(os.path.join(BASE_DIR, "../models/scaler.pkl"))
label_encoder = joblib.load(os.path.join(BASE_DIR, "../models/label_encoder.pkl"))

def predict_disease(symptoms_dict, model_type="rf"):
    """
    symptoms_dict: dict of all features {feature_name: value}
    model_type: "rf" or "nn"
    """
    X_input = pd.DataFrame([symptoms_dict])
    
    if model_type == "nn":
        X_input_scaled = scaler.transform(X_input)
        pred = nn_model.predict(X_input_scaled)
        class_idx = np.argmax(pred, axis=1)[0]
    else:
        class_idx = rf_model.predict(X_input)[0]
    
    disease_name = label_encoder.inverse_transform([class_idx])[0]
    return disease_name
