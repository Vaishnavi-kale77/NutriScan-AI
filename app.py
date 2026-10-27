import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

from predict_and_fetch import (
    predict_food_from_image,
    normalize_food_name_for_api,
    fetch_nutrition_edamam
)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXT = {"png", "jpg", "jpeg", "webp", "jfif", "heic"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if 'food_image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['food_image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    weight = request.form.get("weight", None)

    if weight is None or weight.strip() == "":
        return jsonify({"error": "Weight (grams) is required"}), 400

    try:
        weight = float(weight)
    except ValueError:
        return jsonify({"error": "Weight must be a number"}), 400


    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(save_path)

        # -----------------------------
        # AI MODEL PREDICTION
        # -----------------------------
        predicted_label, confidence = predict_food_from_image(save_path)

        api_food_name = normalize_food_name_for_api(predicted_label)

        try:
            nutrition = fetch_nutrition_edamam(api_food_name, weight)
        except Exception as e:
            return jsonify({"error": "API request failed", "details": str(e)}), 500

        # -----------------------------
        # RESULT DICTIONARY
        # -----------------------------
        result = {
            "predicted_food_label": predicted_label,
            "prediction_confidence": confidence,
            "api_food_query": api_food_name,
            "weight_g": weight,
            "nutrition": {
                "calories": nutrition["calories"],
                "protein_g": nutrition["protein_g"],
                "carbs_g": nutrition["carbs_g"],
                "fat_g": nutrition["fat_g"]
            }
        }

        # Send result to HTML page
        return render_template("index.html", result=result)

    return jsonify({"error": "File type not allowed"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)