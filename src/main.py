import os
import json

import pandas as pd
from DiseaseInfoScraper import DiseaseInfoScraper

DATA_DIR = 'data'
DATA_FILE = 'Training.csv'

def main():

    df = pd.read_csv(os.path.join(DATA_DIR, DATA_FILE))
    diseases = set(df['prognosis'].tolist())

    disease_scraper = DiseaseInfoScraper(diseases)
    disease_data = disease_scraper.get_diseases()

    with open('data.json', 'w') as fp:
        json.dump(disease_data, fp)

    diseases_with_no_data = []
    for disease in disease_data:
        no_data_found = True
        for attr in disease_data[disease]:
            if disease_data[disease][attr]:
                no_data_found = False

        if no_data_found:
            diseases_with_no_data.append(disease)

    print(diseases_with_no_data)

if __name__ == '__main__':
    main()