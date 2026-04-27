from inference_utils import load_best_model, predict_from_features

example = {
    "forks": 40141,
    "open_issues": 299,
    "commit_count": 38349,
    "size": 499189,
    "has_issues": 1,
    "has_projects": 1,
    "has_downloads": 1,
    "has_wiki": 0,
    "has_pages": 0,
    "has_discussions": 0,
    "archived": 0,
    "age_days": 3805,
    "days_since_push": 4,
    "days_since_update": 4,
    "lang_TypeScript": 1,
    "is_org": 1
}

model, scaler, metadata = load_best_model()
predicted = predict_from_features(example, model, scaler, metadata)

print(f"Predicted stars: {predicted}")
print(f"True stars: 418253")

