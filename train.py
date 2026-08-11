"""
Train a real model for AgriShield.

Expected dataset layout:
dataset/
  Tomato___Early_Blight/
  Tomato___Late_Blight/
  Tomato___healthy/
  ...

Example:
  python train.py --data dataset --epochs 12

The script saves model/disease_model.keras and model/labels.json.
For the hackathon, validate on separate FIELD photos; benchmark accuracy
alone is not evidence of field reliability.
"""
import argparse, os, json
import tensorflow as tf
from tensorflow.keras import layers, models

p = argparse.ArgumentParser()
p.add_argument("--train_dir", default="training", help="Path to train directory")
p.add_argument("--val_dir", default="validation", help="Path to test/validation directory")
p.add_argument("--epochs", type=int, default=12)
args = p.parse_args()

IMG = (224, 224)
BATCH = 32

# Load training and validation datasets directly from separate folders
train = tf.keras.utils.image_dataset_from_directory(
    args.train_dir,
    image_size=IMG,
    batch_size=BATCH
)

val = tf.keras.utils.image_dataset_from_directory(
    args.val_dir,
    image_size=IMG,
    batch_size=BATCH
)

labels = train.class_names
os.makedirs("model", exist_ok=True)
with open("model/labels.json", "w") as f:
    json.dump(labels, f)

aug = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(.08),
    layers.RandomZoom(.15),
    layers.RandomContrast(.1)
])

base = tf.keras.applications.EfficientNetB0(include_top=False, weights="imagenet", input_shape=IMG + (3,))
base.trainable = False

inp = layers.Input(shape=IMG + (3,))
x = aug(inp)
x = tf.keras.applications.efficientnet.preprocess_input(x)
x = base(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(.25)(x)
out = layers.Dense(len(labels), activation="softmax")(x)

model = models.Model(inp, out)
model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
              loss="sparse_categorical_crossentropy", 
              metrics=["accuracy"])

model.fit(train, validation_data=val, epochs=args.epochs)
model.save("model/disease_model.keras")
print("Saved model/disease_model.keras")
