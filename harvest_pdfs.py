import time
import requests
import pandas as pd
import os

s = requests.Session()
base_path = "https://www.emerald.com/insight/content/doi/{}/full/pdf"

df = pd.read_csv(os.path.join('doclist', 'oa_articles_clean.csv'), delimiter='\t')
df.sample()

def normalise_doi(doi):
    return doi.replace('.', '_').replace('/', '_')

harvest = True
for doi in df[(
        df['articleTitle'].str.lower().str.contains('covid') |
        df['articleTitle'].str.lower().str.contains('corona') |
        df['articleTitle'].str.lower().str.contains('pandemic')
    )]['DOI'].values[:10]:
    if os.path.exists(os.path.join('source_documents', f'{normalise_doi(doi)}.pdf')):
        continue
    if harvest:
        r = s.get(base_path.format(doi))
        r.raise_for_status
        with open(os.path.join('source_documents', f'{normalise_doi(doi)}.pdf'), 'wb') as f:
            f.write(r.content)
        # rate limiter to avoid a banhammer
        time.sleep(1)