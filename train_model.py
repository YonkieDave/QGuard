import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

print("🚀 Starting Training from LOCAL file...")

# --- 1. LOAD LOCAL DATA ---
try:
    # Read the file you just downloaded and renamed
    data = pd.read_csv("data.csv")
    print(f"✅ Loaded {len(data)} rows from 'data.csv'.")
except FileNotFoundError:
    print("❌ ERROR: Could not find 'data.csv'.")
    print("Please make sure you pasted the file into this folder and renamed it!")
    exit()

# --- 2. CLEAN & PREPARE ---
# Renaming columns to be safe
data.columns = ['url', 'label']

# We use 15,000 rows for a smarter brain (since we have the full file now)
data = data.sample(n=15000, random_state=42)

print("Extracting features (This takes about 10-20 seconds)...")

# --- 3. FEATURE EXTRACTION ---
def get_features(url):
    url = str(url)
    return [
        len(url),
        url.count('.'),
        url.count('@'),
        url.count('-'),
        1 if "https" in url else 0,
        sum(c.isdigit() for c in url)
    ]

X = np.array([get_features(u) for u in data['url']])
y = np.array([1 if l == 'bad' else 0 for l in data['label']])

# --- 4. TRAIN MODEL ---
print("Training QGuard AI...")
model = RandomForestClassifier(n_estimators=50)
model.fit(X, y)

# --- 5. SAVE MODEL ---
with open("phishing_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\n------------------------------------------------")
print("🎉 SUCCESS! 'phishing_model.pkl' is saved.")
print("You are ready to run 'qguard.py'!")
print("------------------------------------------------")