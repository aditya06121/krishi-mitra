import zipfile
import joblib  # or tensorflow/keras/pickle depending on the model format

# Extract the downloaded zip
with zipfile.ZipFile("treeguard.zip", 'r') as zip_ref:
    zip_ref.extractall("model_files")

# Load the model (example for scikit-learn)
model = joblib.load("model_files/model.pkl")
print("Model loaded successfully!")