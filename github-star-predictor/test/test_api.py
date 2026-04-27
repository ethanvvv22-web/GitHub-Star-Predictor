import requests
import json
import numpy as np

BASE_URL = "http://localhost:5000"

## Test the 'predict' endpoint
features = {
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

feature2 = {
    "forks": 441,
    "open_issues": 29,
    "commit_count": 349,
    "size": 4533,
    "has_issues": 10,
    "has_projects": 1,
    "has_downloads": 2,
    "has_wiki": 0,
    "has_pages": 1,
    "has_discussions": 1,
    "archived": 0,
    "age_days": 5,
    "days_since_push": 4,
    "days_since_update": 4,
    "lang_TypeScript": 1,
    "is_org": 1
}


resp = requests.post(f"{BASE_URL}/predict", json=features)
print("Predicted Response: ", resp.json())
  
## Test the '/rank' endpoint
repos = [
	features,
	feature2
]

resp = requests.post(f"{BASE_URL}/rank",json=repos)
print("Rank Responses: ", resp.json())
