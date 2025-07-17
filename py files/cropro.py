# crop_rotation_train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import random
import joblib

# Load your crop dataset
df = pd.read_csv("Crop_recommendation.csv")

# Rule-based simulated next crop mapping
rotation_rules = {
    'rice': ['chickpea', 'lentil'],
    'maize': ['soybean', 'groundnut'],
    'sugarcane': ['wheat'],
    'wheat': ['blackgram', 'sunflower'],
    'mungbean': ['cotton'],
    'banana': ['pigeonpeas'],
    'cotton': ['pearl millet'],
    'default': ['wheat', 'rice']
}

# Simulate 'next_crop'
def recommend_next_crop(crop):
    return random.choice(rotation_rules.get(crop, rotation_rules['default']))

df["next_crop"] = df["label"].apply(recommend_next_crop)

# Prepare features
X = df.drop(columns=["next_crop"])
X["current_crop"] = df["label"]
X = X.drop(columns=["label"])

# Encode the current_crop feature
crop_encoder = LabelEncoder()
X["current_crop"] = crop_encoder.fit_transform(X["current_crop"])

# Target: next crop
y = df["next_crop"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"🔍 Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\n📋 Classification Report:\n", classification_report(y_test, y_pred))

# Save model and encoder
joblib.dump(model, "crop_rotation_model.pkl")
joblib.dump(crop_encoder, "crop_encoder.pkl")
