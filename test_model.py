import os
path = os.path.join("model", "disease_model.keras")
if not os.path.exists(path):
    raise SystemExit(f"Missing model: {path}")
import tensorflow as tf
model = tf.keras.models.load_model(path)
print("MODEL LOADED SUCCESSFULLY")
print("Input shape :", model.input_shape)
print("Output shape:", model.output_shape)
