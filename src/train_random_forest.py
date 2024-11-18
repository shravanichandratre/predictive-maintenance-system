import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Generate dummy data for training
X, y = make_classification(n_samples=100, n_features=5, random_state=42)

# Train a Random Forest model
rf_model = RandomForestClassifier()
rf_model.fit(X, y)

# Save the model
with open("../models/random_forest_model.pkl", "wb") as file:
    pickle.dump(rf_model, file)

print("Random Forest model saved as random_forest_model.pkl in the models folder.")
