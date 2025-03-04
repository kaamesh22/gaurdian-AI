import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

model = load_model("lstm_fatigue_model.h5")

num_samples = 10
heart_rate = np.random.randint(60, 140, num_samples)  
spo2 = np.random.uniform(90, 100, num_samples)  
hrv = np.random.uniform(20, 100, num_samples)  

test_data = pd.DataFrame({
    "Heart_Rate": heart_rate,
    "SpO2": spo2,
    "HRV": hrv
})

scaler = StandardScaler()
test_data_scaled = scaler.fit_transform(test_data)  

test_data_reshaped = test_data_scaled.reshape(test_data_scaled.shape[0], test_data_scaled.shape[1], 1)

predictions = model.predict(test_data_reshaped)

predicted_labels = (predictions > 0.5).astype(int)

for i in range(num_samples):
    print(f"Predicted Stress Level: {predicted_labels[i][0]}")
