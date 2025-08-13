# Models Folder

This folder contains the pre-trained machine learning models used by the AI-Powered Payment Monitoring System.

---

## Files

- `failure_model.pkl`  
  - **Purpose:** Predicts the likelihood of payment failures.  
  - **Expected Interface:** `predict_proba(X)` method to return failure probabilities.  
  - **Notes:** Use any classifier suitable for your data (e.g., Logistic Regression, Random Forest).  

- `fraud_model.pkl`  
  - **Purpose:** Detects potential fraudulent payments.  
  - **Expected Interface:** Anomaly detection method, e.g., `predict(X)` or `score_samples(X)`.  
  - **Notes:** Can be IsolationForest, OneClassSVM, or any custom fraud scorer.  

---

## Usage

1. Place your `.pkl` files in this folder.  
2. The application automatically loads the models at runtime.  
3. If any model is missing, the system will **fallback to baseline heuristics**, so the app remains functional.  

---
