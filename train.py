import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Generate high-quality synthetic data
def generate_synthetic_data(num_samples=10000):
    np.random.seed(42)
    heart_rate = np.random.randint(55, 130, num_samples) 
    spo2 = np.random.uniform(85, 100, num_samples)  
    variability = np.random.uniform(0.5, 2.5, num_samples)  
    stress_level = np.where((heart_rate > 100) & (spo2 < 94) & (variability > 1.5), 1, 0)  
    return pd.DataFrame({'heart_rate': heart_rate, 'spo2': spo2, 'variability': variability, 'stress_level': stress_level})

# Load dataset
df = generate_synthetic_data()

# Normalize data
scaler = MinMaxScaler()
df[['heart_rate', 'spo2', 'variability']] = scaler.fit_transform(df[['heart_rate', 'spo2', 'variability']])

# Prepare sequences for LSTM
X, y = [], []
sequence_length = 20 
for i in range(len(df) - sequence_length):
    X.append(df[['heart_rate', 'spo2', 'variability']].iloc[i:i+sequence_length].values)
    y.append(df['stress_level'].iloc[i+sequence_length])

X, y = np.array(X), np.array(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Define improved LSTM model
model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(sequence_length, 3)),
    BatchNormalization(),
    Dropout(0.3),
    LSTM(64, return_sequences=True),
    BatchNormalization(),
    Dropout(0.3),
    LSTM(32, return_sequences=False),
    BatchNormalization(),
    Dropout(0.2),
    Dense(50, activation='relu'),
    Dense(25, activation='relu'),
    Dense(1, activation='sigmoid')  
])

# Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Save the model
model.save("high_accuracy_fatigue_detection_model.h5")

# Predictions and analysis
y_pred = (model.predict(X_test) > 0.5).astype(int)
accuracy = accuracy_score(y_test, y_pred)

report = classification_report(y_test, y_pred)

print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("Classification Report:")
print(report)
