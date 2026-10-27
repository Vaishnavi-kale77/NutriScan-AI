# NutriScan AI – Automated Nutritional Analysis Using Machine Learning

## 📌 Project Overview

**NutriScan AI** is a machine learning and deep learning-based application that analyzes food images to identify food items and provide nutritional information. The system combines image classification with a nutrition API to help users understand the nutritional value of the food they consume.

Users upload a food image, and the application predicts the food category using a trained deep learning model. It then retrieves nutritional information, such as calories, protein, carbohydrates, and fats, using the Edamam Nutrition API.

The project demonstrates the practical application of computer vision, transfer learning, deep learning, and API integration in food recognition and nutritional analysis.

## 🎯 Objectives

- Identify food items from uploaded images using deep learning.
- Build and evaluate image classification models.
- Integrate food recognition with nutritional information retrieval.
- Display nutritional results through a user-friendly web interface.
- Explore the application of AI in food awareness and dietary tracking.

## ✨ Key Features

- **Food Image Classification:** Predicts the food category from an uploaded image.
- **Deep Learning Models:** Implements and compares multiple CNN-based architectures.
- **Nutritional Information:** Retrieves nutritional data through the Edamam API.
- **Web Application:** Provides an interface for uploading food images and viewing results.
- **Model Evaluation:** Compares classification models using accuracy and validation performance.
- **End-to-End Workflow:** Connects image preprocessing, prediction, API integration, and result presentation.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Machine Learning and Deep Learning:** TensorFlow, Keras, Convolutional Neural Networks (CNN)
- **Computer Vision:** Food image preprocessing and classification
- **Web Framework:** Flask
- **API Integration:** Edamam Nutrition API
- **Dataset:** Food-101
- **Development Environment:** Visual Studio Code
- **Data Handling:** NumPy and related Python libraries, where used in the implementation

## 🧠 Dataset

The project uses the **Food-101 dataset**, a food image dataset containing 101 food categories. It is used to train and evaluate image classification models.

The model learns visual patterns from food images to predict the most likely food category for a new image.

Dataset reference: https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/

## 🤖 Models Implemented

Several deep learning architectures were explored and compared:

| Model | Reported Accuracy |
|---|---:|
| MobileNetV2 | 65% |
| ResNet50 | 63% |
| VGG16 | 61% |
| Custom CNN | 38% |

*Note: These are the project results recorded during experimentation. Performance may vary depending on preprocessing, training configuration, and evaluation methodology.*

MobileNetV2 achieved the highest reported accuracy among the models tested and was explored for food image prediction.

## ⚙️ How It Works

1. **Upload Image:** The user uploads an image of a food item.
2. **Image Preprocessing:** The image is prepared in the format expected by the trained model.
3. **Food Prediction:** The model predicts the food category.
4. **Nutrition Retrieval:** The application uses the predicted food name to request nutritional information from the Edamam API.
5. **Display Results:** The web application presents the prediction and available nutritional details.

## 🏗️ Project Structure

```text
NutriScan-AI/
├── app.py
├── food_classifier.h5
├── label_names.json
├── predict_and_fetch.py
├── script.py
├── train_model.py
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or another Python version compatible with the project's dependencies
- pip
- An Edamam API account and credentials for nutritional information retrieval

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/NutriScan-AI.git
cd NutriScan-AI
```

Replace `YOUR_USERNAME` with your GitHub username.

**2. Create a virtual environment**

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

**3. Install dependencies**

Install the libraries used by your project, such as Flask, TensorFlow, NumPy, and the required HTTP/API client library. If your repository includes a `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

**4. Configure API credentials**

Store your Edamam API credentials in environment variables or a local `.env` file, according to how the application reads its configuration. Never commit API keys or secret credentials to GitHub.

**5. Run the application**

```bash
python app.py
```

Open the local address printed in the terminal by Flask, commonly `http://127.0.0.1:5000/`.

*The exact setup steps depend on the dependencies and configuration used in the current source code.*

## 📊 Results

The project compares four image classification approaches. MobileNetV2 achieved the highest reported accuracy of **65%**, followed by ResNet50 at 63%, VGG16 at 61%, and the custom CNN at 38%.

The application combines the predicted food category with nutrition API integration to demonstrate an end-to-end food recognition workflow.

## 🔮 Future Improvements

- Improve classification accuracy through further training and hyperparameter tuning.
- Expand and validate food recognition across different image conditions.
- Improve food portion-size estimation for more accurate nutritional calculations.
- Enhance API error handling and display clear messages when nutritional information is unavailable.
- Add user history and daily nutrition tracking.
- Deploy the application to a cloud platform for public access.

## 🎓 Learning Outcomes

- Practical experience with deep learning and CNN-based image classification.
- Understanding of transfer learning and model comparison.
- Food image preprocessing and prediction workflows.
- Integration of a third-party nutrition API with a Flask application.
- Development of an end-to-end AI web application.

## 👩‍💻 Project Information

**Project Title:** NutriScan AI – Automated Nutritional Analysis Using Machine Learning

**Domain:** Artificial Intelligence, Machine Learning, Deep Learning, and Computer Vision

**Project Type:** Academic / Final-Year Project

**Developed using:** Python, TensorFlow/Keras, Flask, and Edamam Nutrition API

---

*NutriScan AI explores how machine learning and computer vision can support food recognition and nutritional awareness.*
