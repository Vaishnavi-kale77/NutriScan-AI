# predict_and_fetch.py

import os
import json
import numpy as np
from PIL import Image
import requests
from tensorflow.keras.models import load_model
from dotenv import load_dotenv

load_dotenv()

# API credentials
EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY")
EDAMAM_URL = "https://api.edamam.com/api/nutrition-data"

# Model settings
MODEL_PATH = "food_classifier.h5"
LABELS_PATH = "label_names.json"
IMG_SIZE = 224

# Cache model and labels
_model = None
_labels = None


# --------------------------------------------------
# Load model and labels
# --------------------------------------------------
def load_resources():
    global _model, _labels

    if _model is None:
        _model = load_model(MODEL_PATH)

    if _labels is None:
        with open(LABELS_PATH, "r") as f:
            _labels = json.load(f)

    return _model, _labels


# --------------------------------------------------
# Image preprocessing
# --------------------------------------------------
def preprocess_image_for_prediction(img_path):
    img = Image.open(img_path).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))

    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    return arr


# --------------------------------------------------
# Predict food label
# --------------------------------------------------
def predict_food_from_image(img_path):

    model, labels = load_resources()

    arr = preprocess_image_for_prediction(img_path)

    preds = model.predict(arr)[0]

    class_id = int(np.argmax(preds))
    class_name = labels[class_id]
    confidence = float(preds[class_id])

    return class_name, confidence


# --------------------------------------------------
# Normalize label for API query
# --------------------------------------------------
def normalize_food_name_for_api(food_name):

    food_map = {

        # sandwiches
        "club sandwich": "chicken sandwich",
        "grilled cheese sandwich": "cheese sandwich",

        # burgers
        "hamburger": "beef hamburger",
        "cheeseburger": "cheese hamburger",

        # desserts
        "red velvet cake": "cake",
        "chocolate cake": "cake",
        "cheesecake": "cheesecake",
        "apple pie": "apple pie",
        "ice cream": "ice cream",

        # breakfast
        "omelette": "egg omelette",
        "pancakes": "pancakes",
        "waffles": "waffles",

        # fast food
        "pizza": "cheese pizza",
        "french fries": "potato fries",
        "nachos": "corn chips",

        # pasta / rice
        "spaghetti bolognese": "spaghetti",
        "fried rice": "rice",

        # meat dishes
        "chicken curry": "chicken curry",
        "beef carpaccio": "beef",

        # salad
        "salad": "vegetable salad",

        # fruit fallback
        "apple": "apple",
        "banana": "banana",
        "orange": "orange"
    }

    # Clean label
    s = food_name.lower().replace("_", " ")
    s = "".join(ch for ch in s if (ch.isalnum() or ch.isspace())).strip()

    return food_map.get(s, s)


# --------------------------------------------------
# Fetch nutrition from API
# --------------------------------------------------
def fetch_nutrition_edamam(food_name, weight_grams):

    if not EDAMAM_APP_ID or not EDAMAM_APP_KEY:
        raise RuntimeError("Set EDAMAM_APP_ID and EDAMAM_APP_KEY in .env")

    ingr = f"{weight_grams}g {food_name}"

    print("API Query:", ingr)

    params = {
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY,
        "ingr": ingr
    }

    try:

        response = requests.get(EDAMAM_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        print("Raw API Response:")
        print(json.dumps(data, indent=2))

    except Exception as e:
        print("API error:", e)
        return {
            "calories": 0,
            "protein_g": 0,
            "carbs_g": 0,
            "fat_g": 0,
            "raw_api_response": {}
        }

    # Extract nutrients from API response
    try:
        nutrients = data["ingredients"][0]["parsed"][0]["nutrients"]
        calories = nutrients["ENERC_KCAL"]["quantity"]
        protein = nutrients["PROCNT"]["quantity"]
        carbs = nutrients["CHOCDF"]["quantity"]
        fat = nutrients["FAT"]["quantity"]
    
    except Exception as e:
        print("Parsing error:", e)
        calories = 0
        protein = 0
        carbs = 0
        fat = 0

    return {
        "calories": float(calories),
        "protein_g": float(protein),
        "carbs_g": float(carbs),
        "fat_g": float(fat),
        "raw_api_response": data
    }


# --------------------------------------------------
# Complete pipeline
# --------------------------------------------------
def analyze_food_image(img_path, weight_grams=100):

    predicted_food, confidence = predict_food_from_image(img_path)

    api_food = normalize_food_name_for_api(predicted_food)

    nutrition = fetch_nutrition_edamam(api_food, weight_grams)

    return {
        "predicted_food_label": predicted_food,
        "prediction_confidence": confidence,
        "api_food_query": api_food,
        "nutrition": nutrition,
        "weight_g": weight_grams
    }


# --------------------------------------------------
# Quick test
# --------------------------------------------------
if __name__ == "__main__":

    img_path = input("Enter image path: ")
    weight = input("Enter food weight in grams (default 100): ")

    if weight == "":
        weight = 100
    else:
        weight = int(weight)

    result = analyze_food_image(img_path, weight)

    print(json.dumps(result, indent=2))