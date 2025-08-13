Put your pre-trained pickle files here:
- failure_model.pkl : classifier with predict_proba
- fraud_model.pkl   : anomaly model (IsolationForest/OneClassSVM) or any scorer
- scaler.pkl        : optional
App falls back to heuristics if missing.
