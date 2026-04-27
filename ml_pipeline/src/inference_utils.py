from pathlib import Path
import joblib
import json
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

def load_best_model():
    metadata_path = MODELS_DIR / "best_model_metadata.json"
    model_path = MODELS_DIR / "best_model.joblib"
    
    with open(metadata_path) as f:
        metadata = json.load(f)
        
    model = joblib.load(model_path)
    scaler = joblib.load(metadata["scaler_path"]) if metadata.get("requires_scaling", False) else None
    
    return model, scaler, metadata

def predict_from_features(features, model, scaler=None, metadata=None):
    print("=== NEW VERSION LOADED ===")
    df = pd.DataFrame([features])
    
    for col in model.feature_names_in_:
        if col not in df.columns:
            df[col] = 0
    df = df.reindex(model.feature_names_in_, axis=1)
    
    # if metadata and metadata.get("requires_scaling", False):
    #     numerical = ["forks", "open_issues", "commit_count", "size",
    #                  "age_days", "days_since_push", "days_since_update"]
    #     df[numerical] = scaler.transform(df[numerical])
    if metadata and metadata.get("requires_scaling", False):
        numerical = ["forks", "open_issues", "commit_count", "size",
                     "age_days", "days_since_push", "days_since_update"]

        df[numerical] = scaler.transform(df[numerical].astype(float))
    df = df.astype(float)
    pred = model.predict(df)
    
    if metadata and metadata.get("log_target", False):
        pred = np.expm1(pred)
        
    return round(float(pred[0]))

