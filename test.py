# Load the model
import joblib
model = joblib.load("crop_recommendation_model.pkl")

# Example input: [N, P, K, temperature, humidity, pH, rainfall]
sample_input = [[105, 18, 35, 23.52, 68.44, 6.74, 171.88]]

# Predict crop
predicted_crop = model.predict(sample_input)
print(f"🌾 Recommended Crop: {predicted_crop[0]}")
