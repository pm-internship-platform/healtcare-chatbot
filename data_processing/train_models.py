import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import os

# Try to import TensorFlow/Keras with error handling
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.utils import to_categorical
    TENSORFLOW_AVAILABLE = True
    print("TensorFlow imported successfully")
except ImportError as e:
    print(f"TensorFlow not available: {e}")
    print("Installing TensorFlow with: pip install tensorflow")
    TENSORFLOW_AVAILABLE = False

# Create models folder if not exists
os.makedirs("models", exist_ok=True)

# ---------------- Load preprocessed data ----------------
try:
    X = pd.read_csv("datasets/X.csv")
    y = pd.read_csv("datasets/y.csv").values.ravel()
    print(f"Data loaded successfully: X shape {X.shape}, y shape {y.shape}")
except FileNotFoundError as e:
    print(f"Error loading data: {e}")
    print("Make sure you have run the data preprocessing step first")
    exit(1)

# Ensure all X values are numeric
X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

# Check for any remaining non-numeric values
if X.isnull().any().any():
    print("Warning: Still have NaN values after conversion")
    X = X.fillna(0)

print(f"Feature matrix shape: {X.shape}")
print(f"Number of unique classes: {len(np.unique(y))}")

# ---------------- Train-test split (non-stratified) ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42  # removed stratify=y
)

print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")

# ---------------- Random Forest ----------------
print("\nTraining Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=200, 
    random_state=42,
    n_jobs=-1  # Use all available cores
)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, y_pred_rf)
print(f"Random Forest Accuracy: {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")

# Save Random Forest model
joblib.dump(rf_model, "models/disease_rf_model.pkl")
print("Random Forest model saved as models/disease_rf_model.pkl")

# ---------------- Neural Network (if TensorFlow available) ----------------
if TENSORFLOW_AVAILABLE:
    print("\nTraining Neural Network...")
    
    # Prepare data for neural network
    num_classes = len(np.unique(y))
    
    # Convert labels to categorical
    y_train_cat = to_categorical(y_train, num_classes=num_classes)
    y_test_cat = to_categorical(y_test, num_classes=num_classes)
    
    # Normalize features for neural network
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Build neural network
    nn_model = Sequential([
        Dense(256, input_dim=X_train.shape[1], activation='relu'),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    
    nn_model.compile(
        loss='categorical_crossentropy', 
        optimizer='adam', 
        metrics=['accuracy']
    )
    
    # Train with early stopping to prevent overfitting
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7
    )
    
    # Train the model
    history = nn_model.fit(
        X_train_scaled, y_train_cat,
        epochs=100,
        batch_size=32,
        validation_data=(X_test_scaled, y_test_cat),
        callbacks=[early_stopping, reduce_lr],
        verbose=1
    )
    
    # Evaluate Neural Network
    loss, acc = nn_model.evaluate(X_test_scaled, y_test_cat, verbose=0)
    print(f"Neural Network Accuracy: {acc:.4f} ({acc*100:.2f}%)")
    
    # Save Neural Network model and scaler
    nn_model.save("models/disease_nn_model.h5")
    joblib.dump(scaler, "models/scaler.pkl")
    print("Neural Network model saved as models/disease_nn_model.h5")
    print("Feature scaler saved as models/scaler.pkl")
    
    # Save training history
    history_df = pd.DataFrame(history.history)
    history_df.to_csv("models/training_history.csv", index=False)
    print("Training history saved as models/training_history.csv")

else:
    print("\nSkipping Neural Network training - TensorFlow not available")
    print("To install TensorFlow, run: pip install tensorflow")

print("\nModel training completed!")

# Display model comparison
print("\n" + "="*50)
print("MODEL PERFORMANCE SUMMARY")
print("="*50)
print(f"Random Forest Accuracy: {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")
if TENSORFLOW_AVAILABLE:
    print(f"Neural Network Accuracy: {acc:.4f} ({acc*100:.2f}%)")
print("="*50)
