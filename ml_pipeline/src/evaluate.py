import pandas as pd
import joblib
import json
import os
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from pathlib import Path
from utils import load_dataset_for_model
from model_config import USE_LOG_TARGET
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / 'data'
MODELS_DIR = ROOT_DIR / 'models'
BEST_MODEL_PATH = MODELS_DIR / 'best_model.joblib'
BEST_METADATA_PATH = MODELS_DIR / 'best_model_metadata.json'
METRICS_PATH = MODELS_DIR / 'metrics.json'


def evaluate_models():
    if not METRICS_PATH.exists():
        raise FileNotFoundError(f"Metrics file {METRICS_PATH} does not exist. Please run the training script first.")
    
    with open(METRICS_PATH, 'r') as f:
        metrics = json.load(f)
        
    best_model = None
    best_r2 = float('-inf')
    
    for name, data in metrics.items():
        model_path = Path(data['model_path'])
        if not model_path.exists():
            print(f"Warning: Model file {model_path} does not exist. Skipping evaluation for {name}.")
            continue
        
        X, y, requires_scaling = load_dataset_for_model(name, DATA_DIR)
        _, X_val, _, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        log_target = data.get('log_target', False)
        model = joblib.load(model_path)
        preds = model.predict(X_val)
        if log_target:
            preds = np.expm1(preds)
        r2 = r2_score(y_val, preds)
        
        metrics[name]['r2_val'] = r2
        
        if r2 > best_r2:
            best_r2 = r2
            best_model = {
                "name": name,
                "model": model,
                "path": model_path,
                "r2_val": r2,
                "requires_scaling": requires_scaling,
                "log_target": log_target,
                "params": model.get_params()
            }
    
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=4)
        
    if best_model:
        joblib.dump(best_model['model'], BEST_MODEL_PATH)
        
        metadata = {
            "model_name": best_model['name'],
            "model_path": str(BEST_MODEL_PATH),
            "r2_val": best_model['r2_val'],
            "requires_scaling": best_model['requires_scaling'],
            "params": best_model['params'],
            "scaler_path": str(MODELS_DIR / "scaler.joblib") if best_model["requires_scaling"] else None,
            "log_target": best_model['log_target']
        }
        
        with open(BEST_METADATA_PATH, 'w') as f:
            json.dump(metadata, f, indent=4)
            
        print(f"Best model: {best_model['name']} with R^2: {best_model['r2_val']}")
        print(f"Model saved to {BEST_MODEL_PATH}")
        print(f"Metadata saved to {BEST_METADATA_PATH}")
    else:
        print("No models were evaluated successfully.")

def main():
    evaluate_models()
    
if __name__ == "__main__":
    main()
