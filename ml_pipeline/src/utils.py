import pandas as pd
from pathlib import Path
from model_config import REQUIRES_SCALING

def load_dataset_for_model(model_name, data_dir):

    requires_scaling = REQUIRES_SCALING.get(model_name, False)
    file_name = "github_data_clean_scaled.csv" if requires_scaling else "github_data_clean.csv"
    df_path = data_dir / file_name

    if not df_path.exists():
        raise FileNotFoundError(f"Required dataset file not found: {df_path}")

    df = pd.read_csv(df_path)

    if 'stars' not in df.columns:
        raise ValueError("The dataset must contain a 'stars' column for regression.")

    X = df.drop(columns=["stars"])
    y = df["stars"]

    return X, y, requires_scaling

