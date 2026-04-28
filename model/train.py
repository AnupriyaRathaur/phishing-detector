import pandas as pd
import numpy as np
import tldextract
from sklearn.model_selection import GroupShuffleSplit, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

from model.preprocess import load_phishtank_data, load_legit_data
from features.extractor import extract_features

# =========================
# 1. LOAD DATA
# =========================
print("📥 Loading datasets...")

phish_df = load_phishtank_data("data/online-valid.csv")
legit_df = load_legit_data("data/legit.csv")

print("Original counts:")
print("Phishing:", len(phish_df))
print("Legitimate:", len(legit_df))

# =========================
# 2. BALANCE DATASET
# =========================
# =========================
# 2. CLEAN + BALANCE DATASET
# =========================
print("⚖️ Cleaning & Balancing dataset...")

# ✅ Remove duplicates FIRST
phish_df = phish_df.drop_duplicates(subset=["domain"])
legit_df = legit_df.drop_duplicates(subset=["domain"])

# Normalize
phish_df["domain"] = phish_df["domain"].str.lower().str.strip()
legit_df["domain"] = legit_df["domain"].str.lower().str.strip()

print("After cleaning:")
print("Phishing:", len(phish_df))
print("Legitimate:", len(legit_df))

# ✅ Handle legit dataset size
if len(legit_df) < 1000:
    print("⚠️ Legit dataset too small — using full dataset")
    sample_size = len(legit_df)
else:
    sample_size = 2000

# Balance both
phish_df = phish_df.sample(n=sample_size, random_state=42)
legit_df = legit_df.sample(n=sample_size, random_state=42)

# ✅ Combine AFTER cleaning + balancing
df = pd.concat([phish_df, legit_df]).sample(frac=1, random_state=42).reset_index(drop=True)

print("Balanced counts:")
print(df['label'].value_counts())

# =========================
# 3. GROUPING (ANTI-LEAKAGE)
# =========================
def base_domain(d):
    ext = tldextract.extract(d)
    return f"{ext.domain}.{ext.suffix}"

df["group"] = df["domain"].apply(base_domain)

# =========================
# 4. GROUP SPLIT
# =========================
gss = GroupShuffleSplit(test_size=0.3, n_splits=1, random_state=42)
train_idx, temp_idx = next(gss.split(df, groups=df["group"]))

train_df = df.iloc[train_idx]
temp_df = df.iloc[temp_idx]

gss2 = GroupShuffleSplit(test_size=0.5, n_splits=1, random_state=42)
val_idx, test_idx = next(gss2.split(temp_df, groups=temp_df["group"]))

val_df = temp_df.iloc[val_idx]
test_df = temp_df.iloc[test_idx]

print("Train:", len(train_df))
print("Validation:", len(val_df))
print("Test:", len(test_df))

# =========================
# 5. FEATURE EXTRACTION
# =========================
print("⚙️ Extracting features...")

def extract_data(data):
    X, y = [], []
    for _, row in data.iterrows():
        try:
            feats, _ = extract_features(row['domain'])
            X.append(feats)
            y.append(row['label'])
        except:
            continue
    return np.array(X), np.array(y)

X_train, y_train = extract_data(train_df)
X_val, y_val = extract_data(val_df)
X_test, y_test = extract_data(test_df)

print(f"✅ Features extracted: {len(X_train)+len(X_val)+len(X_test)}")

# =========================
# 6. MODEL TRAINING
# =========================
print("🤖 Training model...")

model = RandomForestClassifier(
    n_estimators=120,
    max_depth=10,   # 🔥 prevent overfitting
    min_samples_split=5,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train, y_train)

print("✅ Model trained")

# =========================
# 7. CROSS VALIDATION
# =========================
scores = cross_val_score(model, X_train, y_train, cv=5)

print("\n🔁 Cross Validation Accuracy:", scores)
print("Mean CV Accuracy:", scores.mean())

# =========================
# 8. EVALUATION
# =========================
y_pred = model.predict(X_test)

print("\n📈 Accuracy:", accuracy_score(y_test, y_pred))

print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

print("\n🧩 Confusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

# =========================
# 9. FEATURE IMPORTANCE
# =========================
print("\n📊 Feature Importance:\n")

feature_names = [
    "length","subdomain","hyphen","digit","entropy",
    "keyword","brand_similarity","risky_tld","idn","mixed_script"
]

importances = model.feature_importances_

for name, score in zip(feature_names, importances):
    print(f"{name}: {score:.4f}")

# =========================
# 10. SAVE MODEL
# =========================
joblib.dump(model, "model/model.pkl")

print("\n💾 Model saved at model/model.pkl")