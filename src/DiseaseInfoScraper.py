import requests
from bs4 import BeautifulSoup

class DiseaseInfoScraper:

    def __init__(self, diseases: set[str]) -> None:
        self.site_link = 'https://www.mayoclinic.org/'
        self.diseases = diseases

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_diseases(self)  -> dict['disease': dict['information': str]]:
        try: 
            diseases_info = dict()
            for disease in self.diseases:
                print(f"Getting Information about {disease}...")
                diseases_info[disease] = self.get_disease(disease)
            return diseases_info
        except:
            return None

    def get_disease(self, disease: str) -> dict['information': str, 'remedies': str]:
        try: 
            disease_page = self.search_disease(disease)

            diagnosis_treatment_page = self.get_diagnosis_treatment_page(disease_page)
            return {
                'overview': self.get_overview(disease, disease_page),
                'symptoms': self.get_symptoms(disease, disease_page),
                'causes': self.get_causes(disease, disease_page),
                'risk_factors': self.get_risk_factors(disease, disease_page),
                'complications': self.get_complications(disease, disease_page),
                'diagnosis': self.get_diagnosis(disease, diagnosis_treatment_page),
                'treatment': self.get_treatment(disease, diagnosis_treatment_page),
            }
        except:
            return None

    def search_disease(self, disease: str) -> BeautifulSoup:
        try: 
            params = {'q': disease}
            url = self.site_link + 'search/search-results'
            response = requests.get(url, params=params, headers=self.headers)

            search_results_page = BeautifulSoup(response.text, 'html.parser')
            disease_link = search_results_page.find(class_='azsearchlink')['href']

            response = requests.get(disease_link, headers=self.headers)
            return BeautifulSoup(response.text, 'html.parser')
        except:
            return None

    def get_overview(self, disease: str, disease_page: BeautifulSoup) -> str:
        try:
            print(f'Getting overview of {disease}...')
            overview = disease_page.find(string='Overview', name='h2')

            information = []
            current = overview.find_next_sibling()

            while 'acces-list-container' not in (current.get('class') if current.get('class') else []):
                if current.text != '':
                    information.append(current.text)
                current = current.find_next_sibling()

            return ' '.join(information)
        except:
            return None

    def get_symptoms(self, disease: str, disease_page: BeautifulSoup) -> str:
        try:
            print(f'Getting symptoms of {disease}...')
            symptoms = disease_page.find(string='Symptoms', name='h2')

            while symptoms.name != 'ul':
                symptoms = symptoms.find_next_sibling() 
        
            return '\n'.join([symptom.text for symptom in symptoms.findAll(name='li')])
        except:
            return None

    def get_causes(self, disease: str, disease_page: BeautifulSoup) -> str:
        try: 
            print(f'Getting causes of {disease}...')
            causes = disease_page.find(string='Causes', name='h2')

            if not causes:
                return None

            causes_info = []
            current = causes.find_next_sibling()
            while current.name == 'p':
                if current.text != '':
                    causes_info.append(current.text)
                current = current.find_next_sibling()

            return '\n'.join(causes_info)
        except:
            return None 

    def get_risk_factors(self, disease: str, disease_page: BeautifulSoup) -> str:
        try: 
            print(f'Getting risk facotrs of {disease}...')
            risk_factors = disease_page.find(string='Risk factors', name='h2')

            while risk_factors.name != 'ul':
                risk_factors = risk_factors.find_next_sibling()

            return '\n'.join([risk.text for risk in risk_factors.findAll(name='li')])
        except:
            return None

    def get_complications(self, disease: str, disease_page: BeautifulSoup) -> str:
        try:
            print(f'Getting complications of {disease}...')
            complications = disease_page.find(string='Complications', name='h2')

            if not complications:
                return None

            complications_info = []
            current = complications.find_next_sibling()
            while current.name == 'p':
                if current.text != '':
                    complications_info.append(current.text)
                current = current.find_next_sibling()

            return '\n'.join(complications_info) 
        except:
            return None

    def get_diagnosis_treatment_page(self, disease_page: BeautifulSoup) -> BeautifulSoup:
        try: 
            link = disease_page.find(class_='sectionnav').find(name='a').get('href')
            response = requests.get(self.site_link + link, headers=self.headers)
            return BeautifulSoup(response.text, 'html.parser')
        except:
            return None

    def get_diagnosis(self, disease: str, diagnosis_treatment_page: BeautifulSoup) -> str:
        try: 
            print(f'Getting diagnosis of {disease}...')
            diagnosis = diagnosis_treatment_page.find(string='Diagnosis', name='h2')

            diagnosis_info = []
            current = diagnosis.find_next_sibling()
            while current.name != 'h2': 
                if current.text != '':
                    diagnosis_info.append(current.text)
                current = current.find_next_sibling()
            return '\n'.join(diagnosis_info)
        except:
            return None


    def get_treatment(self, disease: str, diagnosis_treatment_page: BeautifulSoup) -> str:
        try: 
            print(f'Getting treatment of {disease}...')

            treatment = diagnosis_treatment_page.find(string='Treatment', name='h2')

            treatment_info = []
            current = treatment.find_next_sibling()
            while current.name in ['p', 'h3', 'ul', 'li']:
                if current.text != '':
                    treatment_info.append(current.text)
                current = current.find_next_sibling()
            return '\n'.join(treatment_info)
        except:
            return None

    # def get_prevention(self, disease_page: BeautifulSoup):
    #     prevention = disease_page.find(string='Prevention', name='h2')

    #     if not prevention:
    #         return None

    #     prevention_info = []
    #     current = prevention.find_next_sibling()
    #     while current.get('class') != 'sub':
    #         if current.text != '':
    #             prevention_info.append(current.text)
    #         current = current.find_next_sibling()

    #     return '\n'.join(prevention_info) 