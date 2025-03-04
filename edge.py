import tensorflow as tf

model = tf.keras.models.load_model("high_accuracy_fatigue_detection_model.h5")

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  
tflite_model = converter.convert()

with open("fatigue_model.tflite", "wb") as f:
    f.write(tflite_model)
