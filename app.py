# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# Load models and encoders
crop_recommendation_model = joblib.load("crop_recommendation_model.pkl")
crop_rotation_model = joblib.load("crop_rotation_model.pkl")
crop_encoder = joblib.load("crop_encoder.pkl")

# Load dataset for location & season prediction
crop_data = pd.read_csv("crop_data.csv")

# Crop rotation explanation rules
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

app = Flask(__name__)
CORS(app)

@app.route('/predict-crop', methods=['POST'])
def predict_crop():
    data = request.json
    features = [
        data['N'], data['P'], data['K'],
        data['temperature'], data['humidity'],
        data['ph'], data['rainfall']
    ]
    prediction = crop_recommendation_model.predict([features])[0]
    return jsonify({"recommended_crop": prediction})

@app.route('/predict-by-location', methods=['POST'])
def predict_by_location():
    data = request.json
    state = data['state'].lower()
    district = data['district'].lower()
    season = data['season'].lower()

    filtered = crop_data[
        (crop_data['State'].str.lower() == state) &
        (crop_data['District'].str.lower() == district) &
        (crop_data['Season'].str.lower() == season)
    ]

    if filtered.empty:
        return jsonify({"message": "No crops found for the given criteria."})

    crops = filtered['Crop'].unique().tolist()
    return jsonify({"crops": crops})

@app.route('/predict-next-crop', methods=['POST'])
def predict_next_crop():
    data = request.json
    current_crop = data['current_crop']
    features = [
        data['N'], data['P'], data['K'],
        data['temperature'], data['humidity'],
        data['ph'], data['rainfall']
    ]
    encoded_crop = crop_encoder.transform([current_crop])[0]
    features.append(encoded_crop)

    df_input = pd.DataFrame([features], columns=[
        'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'current_crop'])
    predicted_crop = crop_rotation_model.predict(df_input)[0]

    explanation = rotation_explanations.get(
        (current_crop, predicted_crop),
        rotation_explanations['default']
    )

    return jsonify({
        "current_crop": current_crop,
        "recommended_next_crop": predicted_crop,
        "reason": explanation
    })

if __name__ == '__main__':
    app.run(debug=True)
