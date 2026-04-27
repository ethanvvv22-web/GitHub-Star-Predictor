import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os

np.random.seed(42)
n_samples = 100

data = pd.DataFrame({
	'forks': np.random.randint(0,500,size=n_samples),
	'watchers': np.random.randint(0,1000,size=n_samples),
	'commits': np.random.randint(0,1000,size=n_samples)
})

data['stars'] = (0.5 * data['forks'] +
                 0.3 * data['watchers'] +
                 0.2 * data['commits'] +
                 np.random.normal(0, 50, size=n_samples))  # Add some noise

# Train a model
X = data[['forks', 'watchers', 'commits']]
y = data['stars']

model = LinearRegression()
model.fit(X, y)

with open('./best_model.pkl','wb') as f:
	pickle.dump(model,f)

print('done')
