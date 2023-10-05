import sqlite3

class DiseaseDB:

    def __init__(self) -> None:
        self.db = 'diseases.db'
        print('Connecting to SQLite3 database...')
        self.conn = sqlite3.connect(self.db)
        print('Connected to SQLite3 database...')

        self.init()
    
    def init(self) -> None:
        print('Initializing database...')
        cur = self.conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS diseases (
                disease_name, overview, symptoms, causes,
                risk_factors, complications, diagnosis, treatment
            )
        ''')
        print('Database Initialized')

    def import_diseases_data(self, diseases_info: dict['disease': dict]) -> None:
        print('Importing diseases data...')
        insert_statement = 'INSERT INTO diseases VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        disease_data = [
            (
                disease, 
                diseases_info[disease]['overview'],
                diseases_info[disease]['symptoms'],
                diseases_info[disease]['causes'],
                diseases_info[disease]['risk_factors'],
                diseases_info[disease]['complications'],
                diseases_info[disease]['diagnosis'],
                diseases_info[disease]['treatment'],
            )

            for disease in diseases_info 
            if self.validate_disease(diseases_info[disease])
        ]

        cur = self.conn.cursor()

        cur.executemany(insert_statement, disease_data)
        self.conn.commit()
        print('Imported diseases data...')
    
    def validate_disease(self, disease: dict) -> bool:
        return all(disease[info] for info in disease)
    
    def fetch_disease(self, disease: str) -> tuple:
        fetch_statement = f'SELECT * FROM diseases WHERE disease_name={disease}'
        cur = self.conn.cursor()
        res = cur.execute(fetch_statement)
        return res.fetchone()

    def fetch_diseases(self) -> list[tuple]:
        fetch_statement = 'SELECT * FROM diseases'
        cur = self.conn.cursor()
        res = cur.execute(fetch_statement)
        return res.fetchall()



    