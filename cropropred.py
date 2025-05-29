# crop_rotation_predict.py

import pandas as pd
import joblib

# Load model and encoder
model = joblib.load("crop_rotation_model.pkl")
crop_encoder = joblib.load("crop_encoder.pkl")

# Explanation rules
rotation_explanations = {
    ('rice', 'chickpea'): "Rice depletes nitrogen heavily. Chickpea, a legume, helps restore soil nitrogen.",
    ('rice', 'lentil'): "Rice exhausts nitrogen. Lentil is nitrogen-fixing and ideal for soil recovery.",
    ('maize', 'soybean'): "Maize consumes nutrients. Soybean replenishes soil with nitrogen.",
    ('wheat', 'blackgram'): "Blackgram improves soil texture and fixes nitrogen post wheat.",
    ('wheat', 'sunflower'): "Sunflower helps disrupt wheat disease cycles and balances nutrients.",
    ('cotton', 'pearl millet'): "Cotton attracts pests. Millet rotation reduces pest buildup.",
    ('banana', 'pigeonpeas'): "Pigeonpeas help restore nitrogen post banana farming.",
    'default': "This crop rotation maintains soil health and improves biodiversity."
}

# Example input
current_crop = 'maize'
features = [90, 42, 43, 21.0, 80.0, 6.5, 200.0]  # N, P, K, temp, humidity, pH, rainfall

# Encode crop
encoded_crop = crop_encoder.transform([current_crop])[0]
features.append(encoded_crop)

# Predict
df_input = pd.DataFrame([features], columns=[
    'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'current_crop'
])
predicted_crop = model.predict(df_input)[0]

# Get reason
explanation = rotation_explanations.get(
    (current_crop, predicted_crop),
    rotation_explanations['default']
)

# Output
print(f"🌾 Current Crop: {current_crop}")
print(f"🌱 Recommended Next Crop: {predicted_crop}")
print(f"📌 Reason: {explanation}")
