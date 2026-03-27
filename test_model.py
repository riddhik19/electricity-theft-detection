import joblib
import numpy as np

model = joblib.load('theft_model.pkl')

# Use very extreme low values to trigger suspicious prediction
# Theft = normal * noise(0.3-0.8), so theft has 30-80% of normal values
test_cases = [
    [15.5, 4.2, 25.3, 3.1, 0, 0.27, 22.2],   # Normal
    [1.0, 0.3, 1.8, 0.1, 10, 0.30, 1.7],      # Extreme low - theft
    [0.8, 0.2, 1.5, 0.1, 15, 0.25, 1.4],      # Extreme low - theft
    [0.5, 0.15, 1.0, 0.05, 20, 0.30, 0.95],   # Extreme low - theft
]

print("Testing model predictions:")
for i, X in enumerate(test_cases):
    X = np.array([X])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]
    label = "SUSPICIOUS" if pred == 1 else "Normal"
    print(f"Case {i+1} [{X[0][0]:.1f}]: {label}, Conf={max(prob)*100:.1f}%, Susp={prob[1]*100:.1f}%")

