import tldextract
import math
from Levenshtein import distance

def entropy(domain):
    prob = [domain.count(c)/len(domain) for c in set(domain)]
    return -sum([p * math.log2(p) for p in prob])

def brand_similarity(domain):
    brands = ["google.com", "facebook.com", "amazon.com", "paypal.com"]
    return min(distance(domain, b) for b in brands)

def extract_features(domain):
    ext = tldextract.extract(domain)

    features = {
        "length": len(domain),
        "subdomain_count": len(ext.subdomain.split('.')) if ext.subdomain else 0,
        "hyphen_count": domain.count('-'),
        "digit_count": sum(c.isdigit() for c in domain),
        "entropy": entropy(domain),
        "has_keyword": int(any(k in domain for k in ['login','secure','verify','bank'])),
        "brand_similarity": brand_similarity(domain),
        "is_risky_tld": int(ext.suffix in ['tk','xyz','ml']),
        "is_idn": int("xn--" in domain)
    }

    return list(features.values()), features