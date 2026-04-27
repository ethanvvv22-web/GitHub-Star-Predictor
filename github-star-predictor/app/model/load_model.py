import joblib
import os
import json

model = joblib.load(os.path.join(os.path.dirname(__file__), 'best_model.joblib'))
scaler= joblib.load(os.path.join(os.path.dirname(__file__), 'scaler.joblib'))
with open(os.path.join(os.path.dirname(__file__),'best_model_metadata.json'),'r') as f:
    metadata = json.load(f)

def predict_stars(features):
    import numpy as np
    import pandas as pd

    ## Assumption: features is a dictionary of feature_name: value
    df = pd.DataFrame([features])

    for col in model.feature_names_in_:
        if col not in df.columns:
            df[col] = 0
    df = df.reindex(model.feature_names_in_, axis=1)

    if metadata["requires_scaling"] == True:
        numerical = ['forks', 'open_issues', 'commit_count', 'size', 'age_days', 'days_since_push', 'days_since_update']
        df[numerical] = scaler.transform(df[numerical].astype(float))

    prediction = model.predict(df)[0]
    if metadata["log_target"] == True:
        prediction = np.expm1(prediction)
    return round(float(prediction))
