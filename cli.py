import sys
import joblib
from features.extractor import extract_features

# Load model once
model = joblib.load("model/model.pkl")


def predict(domain):
    features, _ = extract_features(domain)

    pred = model.predict([features])[0]

    probs = model.predict_proba([features])[0]
    label_index = list(model.classes_).index(pred)
    prob = probs[label_index]

    # Avoid showing perfect 1.0 (better presentation)
    prob = min(prob, 0.99)

    return pred, round(prob, 3)


def print_header():
    print("\n" + "="*50)
    print("🔍 PHISHING DETECTION CLI")
    print("="*50 + "\n")


def main():
    if len(sys.argv) < 2:
        print("❌ Usage:")
        print("   python cli.py google.com")
        print("   python cli.py google.com facebook.com paypal-login.xyz")
        return

    domains = sys.argv[1:]

    print_header()

    for domain in domains:
        try:
            pred, prob = predict(domain)

            # Add simple visual indicator
            status_icon = "🟢" if pred == "legitimate" else "🔴"

            print(f"{status_icon} {domain}")
            print(f"   ➤ Prediction : {pred}")
            print(f"   ➤ Confidence : {prob}\n")

        except Exception as e:
            print(f"⚠️ {domain} → Error: {str(e)}\n")


if __name__ == "__main__":
    main()