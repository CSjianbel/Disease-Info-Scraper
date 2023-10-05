import os

import pandas as pd
from DiseaseInfoScraper import DiseaseInfoScraper
from db import DiseaseDB

DATA_DIR = 'data'
DATA_FILE = 'Training.csv'

def main():

    df = pd.read_csv(os.path.join(DATA_DIR, DATA_FILE))
    diseases = set(df['prognosis'].tolist())

    disease_scraper = DiseaseInfoScraper(diseases)
    disease_data = disease_scraper.get_diseases()

    db = DiseaseDB()

    db.import_diseases_data(disease_data)
    db_diseases = db.fetch_diseases()
    print("DATABASE DATA...")
    for disease in db_diseases:
        print(disease)

if __name__ == '__main__':
    main()