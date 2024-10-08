import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Paths to scaler and model files
scaler_path = 'C:/Users/honey/Documents/placment work/Electronical-AI-Device-Recogniser/khanya/AIAPI/scaler1.1.3.pkl'  # Update path as needed
model_path = 'C:/Users/honey/Documents/placment work/Electronical-AI-Device-Recogniser/khanya/AIAPI/appliance_recogniser#1.1.3.keras'     # Update path as needed

# Load the scaler and model
scaler = joblib.load(scaler_path)
model = load_model(model_path)

# Test input (example values)
test_input = np.array([100, 50, 10, 60, 220, 30]).reshape(1, -1)

# Apply the scaler
scaled_input = scaler.transform(test_input)

# Get prediction from the model
predictions = model.predict(scaled_input)

# Output results
print(f"Scaled input: {scaled_input}")
print(f"Raw predictions (probabilities): {predictions}")
print(f"Predicted class: {np.argmax(predictions)}")
