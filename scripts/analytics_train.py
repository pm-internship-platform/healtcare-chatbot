#!/usr/bin/env python3
"""
Script to train predictive outbreak models
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def generate_sample_data():
    """Generate sample outbreak data for training"""
    np.random.seed(42)
    
    # Sample features: temperature, rainfall, humidity, population_density, previous_cases
    n_samples = 1000
    X = np.random.rand(n_samples, 5)
    
    # Generate labels based on feature combinations (simulated outbreak conditions)
    y = np.zeros(n_samples)
    
    # Outbreak conditions (simulated)
    outbreak_conditions = (
        (X[:, 0] > 0.7) &  # High temperature
        (X[:, 1] > 0.6) &  # High rainfall
        (X[:, 4] > 0.5)    # Previous cases
    )
    
    y[outbreak_conditions] = 1
    
    return X, y

def train_outbreak_model():
    """Train the outbreak prediction model"""
    logging.info("Generating training data...")
    X, y = generate_sample_data()
    
    logging.info("Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    logging.info("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5
    )
    
    model.fit(X_train, y_train)
    
    logging.info("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    logging.info(f"Model accuracy: {accuracy:.2f}")
    
    # Save the model
    model_path = "models/outbreak_predictor.pkl"
    joblib.dump(model, model_path)
    logging.info(f"Model saved to {model_path}")
    
    return model, accuracy

def main():
    """Main training function"""
    logging.info("Starting outbreak prediction model training...")
    
    try:
        model, accuracy = train_outbreak_model()
        
        logging.info("Training completed successfully!")
        logging.info(f"Final model accuracy: {accuracy:.2f}")
        
        # Save training metadata
        metadata = {
            "training_date": datetime.now().isoformat(),
            "accuracy": float(accuracy),
            "model_type": "RandomForestClassifier",
            "n_estimators": 100,
            "features": ["temperature", "rainfall", "humidity", "population_density", "previous_cases"]
        }
        
        import json
        with open("models/training_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
            
    except Exception as e:
        logging.error(f"Error during training: {str(e)}")
        raise

if __name__ == "__main__":
    main()