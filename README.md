## Overview

This project combines a machine learning pipeline with a Flask-based API to predict GitHub repository stars. 

The ML pipeline consists of three steps: data preprocessing (`preprocess.py`), model training (`train_model.py`), and evaluation (`evaluate.py`). The best model is selected based on the validation R² score, and the resulting artifacts (`best_model.joblib`, `scaler.joblib`, and metadata) are used by the application.

The system is containerized using Docker, with separate services for the ML pipeline and the Flask application. 
## Result
<img width="1281" height="846" alt="image" src="https://github.com/user-attachments/assets/52b84d94-b24d-4bca-acb6-89b75738c653" />
