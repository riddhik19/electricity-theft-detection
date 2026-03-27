import joblib
import pandas as pd
import numpy as np

model = joblib.load('theft_model.pkl')
model_features = ['mean', 'std', 'max', 'min', 'zero_days', 'cv', 'range']

df = pd.read_csv('sample_data.csv')

print("Sample data predictions with LOW THRESHOLD (0.25):")
suspicious_count = 0
for idx, row in df.iterrows():
    X = np.array([row[model_features].values])
    probs = model.predict_proba(X)[0]
    pred = 1 if probs[1] > 0.25 else 0  # LOW threshold
    label = "Suspicious" if pred == 1 else "Normal"
    conf = max(probs)*100
    susp_prob = probs[1]*100
    if pred == 1:
        suspicious_count += 1
    print(f"Row {idx+1} mean={row['mean']:.1f}: {label} (Conf={conf:.1f}%, Susp={susp_prob:.1f}%)")
    if idx > 9: break

print(f"\nTotal suspicious in first 10 rows: {suspicious_count}")

