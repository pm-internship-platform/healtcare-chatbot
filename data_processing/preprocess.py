import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

# Load merged dataset (ignore low_memory warning)
df = pd.read_csv("datasets/merged_dataset.csv", low_memory=False)

# Convert all symptom columns to numeric (non-numeric → 0)
symptom_cols = df.columns[:-1]  # all except 'disease'
for col in symptom_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)  # convert strings to 0
    df[col] = df[col].apply(lambda x: 1 if x > 0 else 0)  # binary

# Encode disease labels
le = LabelEncoder()
df['disease'] = le.fit_transform(df['disease'].astype(str))

# Save LabelEncoder
joblib.dump(le, "models/label_encoder.pkl")
print("LabelEncoder saved as models/label_encoder.pkl")

# Split features and target
X = df[symptom_cols]
y = df['disease']

# Save preprocessed data for training
X.to_csv("datasets/X.csv", index=False)
y.to_csv("datasets/y.csv", index=False)
print("Preprocessed data saved as datasets/X.csv and datasets/y.csv")
