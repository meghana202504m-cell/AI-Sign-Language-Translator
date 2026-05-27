import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

# ✅ Load combined gesture data
data_path = "combined_gesture_data.csv"

# Safety check: file exists and is not empty
if not os.path.exists(data_path) or os.path.getsize(data_path) == 0:
    print("🚫 combined_gesture_data.csv is missing or empty. Please collect and combine gesture data first.")
    exit()

df = pd.read_csv(data_path)

# Safety check: DataFrame is not empty
if df.empty:
    print("🚫 No data found in combined_gesture_data.csv. Please verify your gesture files.")
    exit()

# ✅ Prepare features and labels
if 'label' not in df.columns:
    print("🚫 'label' column missing in dataset.")
    exit()

X = df.drop('label', axis=1)
y = df['label']

# ✅ Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train Random Forest model
print("🔄 Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ✅ Evaluate model
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))

# ✅ Save model using pickle
with open("sign_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("🎉 Model saved as sign_model.pkl")
