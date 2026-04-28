import pandas as pd

# generate many realistic domains
base = [
    "google","facebook","amazon","microsoft","apple","netflix","linkedin",
    "github","twitter","instagram","reddit","yahoo","bing","zoom","dropbox",
    "spotify","adobe","salesforce","paypal","stackoverflow"
]

tlds = [".com",".org",".net",".io",".co"]

domains = []

for b in base:
    for t in tlds:
        domains.append(b+t)

# add variations
for i in range(2000):
    domains.append(f"site{i}.com")

df = pd.DataFrame({
    "domain": list(set(domains)),
    "label": "legitimate"
})

df.to_csv("data/legit.csv", index=False)

print("✅ Legit dataset created:", len(df))