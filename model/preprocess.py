import pandas as pd
from urllib.parse import urlparse

# Extract domain from URL
def extract_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return None

# Load phishing dataset (PhishTank)
def load_phishtank_data(path):
    df = pd.read_csv(path)

    # keep only URL column
    df = df[['url']].dropna()

    # extract domain
    df['domain'] = df['url'].apply(extract_domain)

    # remove empty
    df = df[df['domain'] != ""]

    df['label'] = 'phishing'

    return df[['domain', 'label']]

# Load legit dataset
def load_legit_data(path):
    df = pd.read_csv(path)

    df = df[['domain']].dropna()
    df['label'] = 'legitimate'

    return df

# Combine both datasets
def combine_data(phish_df, legit_df):
    df = pd.concat([phish_df, legit_df])

    # remove duplicates
    df = df.drop_duplicates(subset='domain')

    return df