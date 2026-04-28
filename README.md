Phishing Domain Detection System
1. Setup and Installation
##Clone Repository
git clone https://github.com/AnupriyaRathaur/phishing-detector.git
cd phishing-detector

##Create Virtual Environment (Optional but Recommended)
python -m venv myenv
myenv\Scripts\activate   # Windows
🔹 Install Dependencies
pip install -r requirements.txt

2. Dataset Download & Preparation
🔹 Phishing Dataset
Download from PhishTank:
👉 http://data.phishtank.com/data/online-valid.csv
Save in:
data/online-valid.csv
🔹 Legitimate Dataset
Use Tranco Top Domains:
👉 https://tranco-list.eu/
Convert into CSV format:
domain,label
google.com,legitimate
facebook.com,legitimate
amazon.com,legitimate
...
Save in:
data/legit.csv

3. Train the Model
Run the following command:
python -m model.train
This will:
Load datasets
Extract features
Train RandomForest model
Evaluate performance
Save model to:
model/model.pkl

4. Start API Server
Run:
uvicorn api.main:app --reload
Open Swagger UI:
👉 http://127.0.0.1:8000/docs
🔌 5. API Documentation
🔹 1. Predict Single Domain
Endpoint:
POST /api/predict
Request:

{
  "domain": "secure-login-paypal.xyz"
}

Response:

{
  "domain": "secure-login-paypal.xyz",
  "label": "phishing",
  "confidence": 1,
  "features": {
    "length": 23,
    "subdomain_count": 0,
    "hyphen_count": 2,
    "digit_count": 0,
    "entropy": 4.001822825622231,
    "has_keyword": 1,
    "brand_similarity": 16,
    "is_risky_tld": 1,
    "is_idn": 0
  }
}

2. Batch Prediction

Endpoint:
POST /api/predict/batch
Request:

[
  "google.com",
  "facebook.com",
  "secure-login-paypal.xyz"
]

Response:

[
  {"domain": "google.com", "label": "legitimate"},
  {"domain": "facebook.com", "label": "legitimate"},
  {"domain": "secure-login-paypal.xyz", "label": "phishing"}
]
3. Statistics API

Endpoint:
GET /api/stats

Response:

{
  "total": 100,
  "phishing": 60,
  "legitimate": 40
}

6. Model Performance

Metric	Value
Accuracy	98.7%
Precision	99%
Recall	99%
F1 Score	99%
Confusion Matrix
[[300   3]
 [  5 350]]

8. Feature Engineering

The following features are extracted:

Domain length
Number of subdomains
Hyphen count
Digit count
Entropy of domain
Presence of phishing keywords
Brand similarity (Levenshtein distance)
Risky TLD detection (.tk, .xyz, etc.)
IDN (Internationalized domain) detection

8. Design Decisions
Used RandomForestClassifier for:
High accuracy
Interpretability
Fast training
Used balanced dataset to avoid bias
Used group-based splitting to prevent data leakage
API built using FastAPI for high performance
MongoDB used for storing prediction logs

9. Assumptions
Only domain-level features used (no WHOIS dependency)
Real-time DNS lookup not required
Dataset quality impacts model performance
Legitimate dataset must contain diverse domains

10. CLI Usage
python cli.py google.com facebook.com paypal-login.xyz

11. Database

MongoDB is used to store predictions.

Database: phishing_db
Collection: predictions





