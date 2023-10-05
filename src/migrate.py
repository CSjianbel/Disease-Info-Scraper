import json

from db import DiseaseDB

JSON_FILE = 'data.json'

def main():

    # Read data.json to python dictionary
    with open(JSON_FILE, 'r') as fp:
        data = json.load(fp)

    # Initialize database
    db = DiseaseDB()

    # Migrate json data to database
    db.import_diseases_data(data)

if __name__ == '__main__':
    main()