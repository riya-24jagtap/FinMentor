import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from scipy.stats import mode

import sklearn_crfsuite
from hmmlearn import hmm

# ---------------- LOAD DATA ----------------
df = pd.read_excel(r"D:\riya\Finmentor_Data_REDESIGNED.xlsx")

features = [
    "monthly_income",
    "total_expense",
    "total_emi",
    "emi_ratio",
    "expense_ratio",
    "savings_behaviour",
    "emi_status",
    "spending_behaviour",
    "net_balance",
    "savings_rate"
]

TARGET = "persona"

# ---------------- ENCODE CATEGORICAL ----------------
df["savings_behaviour"] = df["savings_behaviour"].map({
    "Good Saver": 0,
    "Low Saver": 1
})

df["spending_behaviour"] = df["spending_behaviour"].map({
    "Moderate Spender": 0,
    "High Spender": 1
})

df["emi_status"] = df["emi_status"].map({
    "Normal EMI": 1,
    "High EMI Burden": 0
})

# Encode target
label_encoder = LabelEncoder()
df[TARGET] = label_encoder.fit_transform(df[TARGET])

X = df[features].values
y = df[TARGET].values

# ---------------- TRAIN-TEST SPLIT (STRATIFIED) ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------- SCALE (NO DATA LEAKAGE) ----------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =========================================================
# ====================== SVM ==============================
# =========================================================
svm_model = SVC(
    kernel="rbf",
    probability=True,
    class_weight="balanced"
)

svm_model.fit(X_train_scaled, y_train)
svm_pred = svm_model.predict(X_test_scaled)

print("\n----- SVM Results -----")
print("Accuracy:", accuracy_score(y_test, svm_pred))
print(classification_report(y_test, svm_pred))


# =========================================================
# ====================== HMM ==============================
# (Unsupervised - kept for comparison only)
# =========================================================
hmm_model = hmm.GaussianHMM(
    n_components=len(np.unique(y)),
    covariance_type="diag",
    n_iter=100
)

hmm_model.fit(X_train_scaled)
hmm_pred = hmm_model.predict(X_test_scaled)

print("\n----- HMM Results (Unsupervised) -----")
print("Accuracy:", accuracy_score(y_test, hmm_pred))
print(classification_report(y_test, hmm_pred))


# =========================================================
# ====================== CRF ==============================
# =========================================================

def row_to_features(row):
    return {features[i]: row[i] for i in range(len(features))}

# Use SAME train-test split as SVM
X_train_crf = [[row_to_features(row)] for row in X_train_scaled]
X_test_crf  = [[row_to_features(row)] for row in X_test_scaled]

y_train_crf = [[str(label)] for label in y_train]
y_test_crf  = [[str(label)] for label in y_test]

crf_model = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    max_iterations=100,
    all_possible_transitions=True
)

crf_model.fit(X_train_crf, y_train_crf)

y_pred_crf = crf_model.predict(X_test_crf)
y_pred_crf_flat = np.array([int(label[0]) for label in y_pred_crf])

print("\n----- CRF Results -----")
print("Accuracy:", accuracy_score(y_test, y_pred_crf_flat))
print(classification_report(y_test, y_pred_crf_flat))


# =========================================================
# ====================== ENSEMBLE =========================
# (SVM + CRF HARD VOTING)
# =========================================================

all_preds = np.vstack((svm_pred, y_pred_crf_flat))
ensemble_pred = mode(all_preds, axis=0)[0].flatten()

print("\n===== FINAL ENSEMBLE RESULTS =====")
print("Accuracy:", accuracy_score(y_test, ensemble_pred))
print(classification_report(y_test, ensemble_pred))


# =========================================================
# ================= SAVE MODELS ===========================
# =========================================================

save_path = r"D:\riya\FinMentor\fintechsnap\ml_models"
os.makedirs(save_path, exist_ok=True)

joblib.dump(svm_model, os.path.join(save_path, "svm_model.pkl"))
joblib.dump(hmm_model, os.path.join(save_path, "hmm_model.pkl"))
joblib.dump(crf_model, os.path.join(save_path, "crf_model.pkl"))
joblib.dump(scaler, os.path.join(save_path, "scaler.pkl"))

print("\nAll models saved successfully.")