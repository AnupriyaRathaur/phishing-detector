from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List
from services.db import collection


from services.predictor import predict_single
from utils.stats import update_stats, get_stats

app = FastAPI(title="Phishing Detection API 🚀")

# =========================
# Request Schemas
# =========================

class DomainRequest(BaseModel):
    domain: str

    @validator("domain")
    def validate_domain(cls, v):
        if "." not in v:
            raise ValueError("Invalid domain")
        return v


class BatchRequest(BaseModel):
    domains: List[str]

# =========================
# Routes
# =========================

@app.get("/")
def home():
    return {"message": "Phishing Detection API Running 🚀"}

# ✅ 1. SINGLE PREDICTION
@app.post("/api/predict")
def predict(req: DomainRequest):
    result = predict_single(req.domain)
    return result 

# ✅ 2. BATCH PREDICTION
@app.post("/api/predict/batch")
def predict_batch(domains: list[str]):
    results = []
    for d in domains:
        results.append(predict_single(d))
    return results


# ✅ 3. STATS API
@app.get("/api/stats")
def stats():
    total = collection.count_documents({})
    phishing = collection.count_documents({"label": "phishing"})
    legit = collection.count_documents({"label": "legitimate"})

    return {
        "total": total,
        "phishing": phishing,
        "legitimate": legit
    }


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/api/db")
def get_data():
    data = list(collection.find())
    return [serialize(d) for d in data]