import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

# Define paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / 'data'
MODELS_DIR = ROOT_DIR / 'models'
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Load data
data_file = DATA_DIR / "github_repos_data.csv"
df = pd.read_csv(data_file)

# Parse dates and compute age/delta columns
df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
df["pushed_at"] = pd.to_datetime(df["pushed_at"], utc=True)
df["updated_at"] = pd.to_datetime(df["updated_at"], utc=True)
now = pd.Timestamp.now(tz="UTC")

df["age_days"] = (now - df["created_at"]).dt.days
df["days_since_push"] = (now - df["pushed_at"]).dt.days
df["days_since_update"] = (now - df["updated_at"]).dt.days

# Drop fields we don't need
df.drop(columns=["created_at", "pushed_at", "updated_at", "watchers", "name", "topics"], inplace=True, errors="ignore")

# Handle booleans
df["language"] = df["language"].fillna("Unknown")
df.drop(columns=["is_template", "allow_forking"], inplace=True, errors='ignore')
kept_bool_cols = ['has_issues', 'has_projects', 'has_pages', 'has_discussions', 'archived', 'has_wiki', 'has_downloads']
df[kept_bool_cols] = df[kept_bool_cols].astype(int)

# Handle languages
top_languages = df['language'].value_counts().nlargest(10).index
df['language_grouped'] = df['language'].apply(lambda x: x if x in top_languages else 'Other')
df = pd.get_dummies(df, columns=['language_grouped'], prefix='lang')
df.drop(columns=["language"], inplace=True)

# Organization info
df["is_org"] = (df["owner_type"] == "Organization").astype(int)
df.drop(columns=["owner_type"], inplace=True)

# Save unscaled clean version
df.to_csv(DATA_DIR / "github_data_clean.csv", index=False)
 
# Scale selected numerical columns
numerical_features = [
    "forks", "open_issues", "commit_count", "size",
    "age_days", "days_since_push", "days_since_update"
]
scaler = StandardScaler()
scaled_numerical = pd.DataFrame(
    scaler.fit_transform(df[numerical_features]),
    columns=numerical_features
)

# Save the scaler
joblib.dump(scaler, MODELS_DIR / "scaler.joblib")

# Combine with other features
non_num_features = df.drop(columns=["stars"] + numerical_features)
df_scaled = pd.concat([scaled_numerical, non_num_features], axis=1)
df_scaled["stars"] = df["stars"]

# Save scaled dataset
df_scaled.to_csv(DATA_DIR / "github_data_clean_scaled.csv", index=False)

print("Preprocessing complete.")
print("Saved:")
print(f"- {DATA_DIR / 'github_data_clean.csv'}")
print(f"- {DATA_DIR / 'github_data_clean_scaled.csv'}")
print(f"- {MODELS_DIR / 'scaler.joblib'}")

