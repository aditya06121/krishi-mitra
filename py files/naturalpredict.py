import joblib
import pandas as pd
import re
import spacy

# Load NLP model for entity extraction
nlp = spacy.load("en_core_web_sm")

# Load classifiers
vec = joblib.load("intent_vectorizer.pkl")
clf = joblib.load("intent_classifier.pkl")
model1 = joblib.load("crop_recommendation_model.pkl")  # NPK model
model2 = joblib.load("crop_encoder.pkl")               # State-season model
model3 = joblib.load("crop_rotation_model.pkl")        # Crop rotation

# Get user question
question = input("🧑‍🌾 Ask your question: ")

# Predict intent
X_test = vec.transform([question])
intent = clf.predict(X_test)[0]

# Run NLP pipeline
doc = nlp(question)

# Utility functions
def extract_numbers(text):
    return list(map(float, re.findall(r'\d+(?:\.\d+)?', text)))

def extract_season(text):
    seasons = ['Kharif', 'Rabi', 'Zaid', 'Whole Year']
    for s in seasons:
        if s.lower() in text.lower():
            return s
    return None

def extract_crop(text):
    crops = ['rice', 'wheat', 'maize', 'cotton', 'sugarcane', 'banana', 'mungbean']
    for c in crops:
        if c in text.lower():
            return c
    return None

def extract_state_and_district(text):
    # Add your actual state and district list here
    states = ['Karnataka', 'Tamil Nadu', 'Maharashtra', 'Punjab', 'Bihar']
    districts = ['Gulbarga', 'Belgaum', 'Nagpur', 'Chennai', 'Patna']

    found_state, found_district = None, None
    for word in text.split():
        word_clean = word.strip().title()
        if word_clean in states and not found_state:
            found_state = word_clean
        elif word_clean in districts and not found_district:
            found_district = word_clean

    return found_state, found_district


# Handle based on intent
if intent == 1:
    print("🔍 Using Model 1 (Soil-based Crop Recommender)")
    numbers = extract_numbers(question)
    if len(numbers) < 7:
        print("❗ Please include N, P, K, temperature, humidity, pH, and rainfall in your question.")
    else:
        features = numbers[:7]
        prediction = model1.predict([features])
        print("✅ Recommended Crop:", prediction[0])

elif intent == 2:
    print("🌍 Using Model 2 (Location & Season Recommender)")
    state, district = extract_state_and_district(question)
    season = extract_season(question)
    if not (state and district and season):
        print("❗ Please include state, district, and season in your question.")
    else:
        df_input = pd.DataFrame([[state, district, season]], columns=["State", "District", "Season"])
        prediction = model2.predict(df_input)
        print(f"✅ Recommended Crop for {district}, {state} in {season}: {prediction[0]}")

elif intent == 3:
    print("🔄 Using Model 3 (Crop Rotation Advisor)")
    crop = extract_crop(question)
    numbers = extract_numbers(question)
    if not crop or len(numbers) < 7:
        print("❗ Please mention current crop and basic soil info (NPK, pH, rainfall, etc.).")
    else:
        features = numbers[:7]
        df_input = pd.DataFrame([features + [crop]], columns=[
            'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'current_crop'
        ])
        prediction = model3.predict(df_input)[0]
        print(f"✅ Suggested next crop after {crop}: {prediction}")
        print(f"📘 Reason: {crop} depletes specific nutrients. {prediction} supports soil recovery.")
