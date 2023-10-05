import os
import json

import pandas as pd
from DiseaseInfoScraper import DiseaseInfoScraper

DATA_DIR = 'data'
DATA_FILE = 'Training.csv'

def main():

    # Get all diseases to be scraped 
    df = pd.read_csv(os.path.join(DATA_DIR, DATA_FILE))
    diseases = set(df['prognosis'].tolist())

    # scrape disease info
    disease_scraper = DiseaseInfoScraper(diseases)
    disease_data = disease_scraper.get_diseases()

    # Save data to json that will then be migrated to a DB
    with open('data.json', 'a') as fp:
        json.dump(disease_data, fp)

if __name__ == '__main__':
    main()

