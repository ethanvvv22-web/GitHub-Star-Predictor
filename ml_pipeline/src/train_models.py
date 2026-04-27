import pandas as pd

import joblib
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json
import os
from datetime import datetime
from pathlib import Path
from utils import load_dataset_for_model
from model_config import USE_LOG_TARGET
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / 'data'
MODELS_DIR = ROOT_DIR / 'models'

models = {
    "linear_regression": LinearRegression(),
    "random_forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "svm": SVR(kernel='rbf', C=1.0, epsilon=0.2),
    "mlp": MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42),
    "decision_tree": DecisionTreeRegressor(max_depth=10, random_state=42),
    "xgboost": XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
}


def train_models():
    metrics = {}

    for name, model in models.items():
        print(f"\n{'=' * 50}")
        print(f"Training {name}...")
        print(f"{'=' * 50}")

        X, y, requires_scaling = load_dataset_for_model(name, DATA_DIR)

        # ✅ 正确获取训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        use_log_target = USE_LOG_TARGET.get(name, False)

        y_train_orig = y_train.copy()
        y_test_orig = y_test.copy()

        # Apply log transformation to target variable if specified
        if use_log_target:
            y_train = np.log1p(y_train)
            y_test = np.log1p(y_test)

        # ✅ 实际应用特征缩放
        scaler = None
        if requires_scaling:
            print(f"  Applying StandardScaler...")
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

        # Train model
        model.fit(X_train, y_train)

        # ✅ 在测试集上预测
        preds = model.predict(X_test)

        # Convert predictions back if log transformation was used
        if use_log_target:
            preds = np.expm1(preds)

        # ✅ 计算多个指标
        r2 = r2_score(y_test_orig, preds)
        mae = mean_absolute_error(y_test_orig, preds)
        rmse = np.sqrt(mean_squared_error(y_test_orig, preds))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = MODELS_DIR / f"{name}_{timestamp}.joblib"

        # ✅ 保存模型和scaler
        save_data = {
            'model': model,
            'scaler': scaler
        }
        joblib.dump(save_data, model_path)

        metrics[name] = {
            "r2_score": float(r2),
            "mae": float(mae),
            "rmse": float(rmse),
            "model_path": str(model_path),
            "requires_scaling": requires_scaling,
            "params": model.get_params(),
            "log_target": use_log_target
        }

        print(f"  R² Score: {r2:.4f}")
        print(f"  MAE: {mae:.1f}")
        print(f"  RMSE: {rmse:.1f}")
        print(f"  Model saved to: {model_path.name}")

    metrics_path = MODELS_DIR / 'metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)

    print(f"\n{'=' * 50}")
    print("Training complete. Models and metrics saved.")
    print(f"Metrics file: {metrics_path}")
    print(f"{'=' * 50}")


def main():
    MODELS_DIR.mkdir(exist_ok=True)
    train_models()


if __name__ == "__main__":
    main()