# train_model.py
import os
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

# PARAMETERS
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 8   # increase for final training
MODEL_PATH = "food_classifier.h5"

def preprocess(image, label):
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    image = image / 255.0
    return image, label

def prepare_datasets():
    # Using TFDS Food101 as an example
    ds_train, ds_val = tfds.load('food101', split=['train', 'validation'], as_supervised=True)
    ds_train = ds_train.map(preprocess).shuffle(2048).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    ds_val = ds_val.map(preprocess).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    info = tfds.builder('food101').info
    num_classes = info.features['label'].num_classes
    label_names = info.features['label'].names
    return ds_train, ds_val, num_classes, label_names

def build_model(num_classes):
    base_model = MobileNetV2(include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3), weights="imagenet")
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(512, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax")
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def main():
    train_ds, val_ds, num_classes, label_names = prepare_datasets()
    model = build_model(num_classes)

    model.summary()
    model.fit(train_ds, epochs=EPOCHS, validation_data=val_ds)
    model.save(MODEL_PATH)

    # Save label mapping
    import json
    with open("label_names.json", "w") as f:
        json.dump(label_names, f)

    print("Model and label mapping saved.")

if __name__ == "__main__":
    main()
