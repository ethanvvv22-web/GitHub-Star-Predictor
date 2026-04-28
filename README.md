🚀 GitHub Star Prediction System (ML Pipeline + Flask API)

📌 Overview

This project builds an end-to-end machine learning system to predict GitHub repository stars. It combines a modular ML pipeline with a Flask-based API for real-time prediction and ranking.

The system is designed with a layered architecture, covering data processing, model training, inference, and deployment.

🚀 Key Features

📊 End-to-end ML pipeline (preprocess → train → evaluate)

🤖 Model selection based on validation performance (R²)

⚙️ Configuration-driven design (model-aware preprocessing)

🧠 Dedicated inference layer for prediction logic

🌐 REST API for prediction and ranking

🎨 Interactive web interface

🐳 Dockerized deployment

🧠 System Design

The project follows a layered machine learning system architecture:

Data Layer → Training Layer → Inference Layer → Application Layer

🔹 Data Layer
Handles data preprocessing and feature engineering
Implemented in preprocess.py

🔹 Training Layer
Trains and evaluates multiple models
Selects the best model based on R² score
Implemented in train_models.py and evaluate.py

🔹 Inference Layer 
Loads model and scaler
Applies consistent preprocessing to inputs
Encapsulates prediction logic for reuse
Implemented in:
inference_utils.py
model_config.py
inference_test.py

🔹 Application Layer
Exposes prediction services via Flask API
Provides a simple web UI
Implemented in app.py

🧠 Machine Learning Pipeline

The training workflow consists of three main steps:

python preprocess.py
python train_model.py
python evaluate.py
Data is cleaned and transformed
Multiple models can be trained
The best model is selected based on validation R² score

📦 Model Artifacts

After training, the following files are required for inference:

app/model/

├── best_model.joblib

├── scaler.joblib

├── best_model_metadata.json

model → performs prediction

scaler → ensures consistent input preprocessing

metadata → stores model information (R², model type, etc.)

🌐 API Endpoints

🔮 Predict Stars
POST /predict

Input:

{
  "forks": 100,
  
  "open_issues": 10
}

🌐 API Output

Output:

{
  "predicted_stars": 1234
}
📈 Rank Repositories

POST /rank

Input:
List of repositories

Output:
Ranked list based on predicted stars

## 🏗️ Project Structure

.
├── app/                     # Flask application (API + UI)

│   ├── model/               # Model artifacts

│   └── app.py

├── ml_pipeline/

│   ├── src/

│   │   ├── preprocess.py

│   │   ├── train_models.py

│   │   ├── evaluate.py

│   │   ├── inference_utils.py

│   │   ├── model_config.py

│   │   ├── inference_test.py

│   │   └── utils.py

├── docker-compose.yml

├── requirements.txt

├── README.md

##🐳 Running with Docker
docker compose up --build

##🧰 Tech Stack
Python
Scikit-learn / XGBoost
Pandas / NumPy
Flask
Docker

##📝 Notes
Model files must exist in app/model/ before running
Docker is recommended for consistent environments
Kubernetes setup is optional

##🎯 Key Takeaways
Demonstrates a complete ML system (not just a model)
Separates training and inference logic
Uses configuration-driven design
Shows ability to build deployable ML applications
## Result
<img width="1281" height="846" alt="image" src="https://github.com/user-attachments/assets/52b84d94-b24d-4bca-acb6-89b75738c653" />
