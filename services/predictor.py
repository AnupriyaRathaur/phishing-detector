import joblib
from features.extractor import extract_features
from services.db import save_result

model = joblib.load("model/model.pkl")

def predict_single(domain: str):
    features, raw = extract_features(domain)

    pred = model.predict([features])[0]

    probs = model.predict_proba([features])[0]
    label_index = list(model.classes_).index(pred)
    prob = probs[label_index]

    result = {
        "domain": str(domain),
        "label": str(pred),
        "confidence": float(prob),
        "features": raw
    }

    # ✅ Save to DB (ignore returned ObjectId)
    save_result(result.copy())

    # ✅ FORCE clean JSON (important)
    return {
        "domain": result["domain"],
        "label": result["label"],
        "confidence": result["confidence"],
        "features": result["features"]
    }