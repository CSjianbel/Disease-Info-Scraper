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
        diseases_info = dict()
        for disease in self.diseases:
            diseases_info[disease] = self.get_disease(disease)
        return diseases_info

    def get_disease(self, disease: str) -> dict['information': str, 'remedies': str]:
        disease_page = self.search_disease(disease)
        return {
            # 'information': self.get_information(disease_page),
            'symptoms': self.get_symptoms(disease_page),
            # 'remedies': self.get_remedies(disease_page),
        }

    def search_disease(self, disease: str) -> BeautifulSoup:
        params = {'q': disease}
        url = self.site_link + 'search/search-results'
        response = requests.get(url, params=params, headers=self.headers)

        search_results_page = BeautifulSoup(response.text, 'html.parser')
        disease_link = search_results_page.find(class_='azsearchlink')['href']

        response = requests.get(disease_link, headers=self.headers)
        return BeautifulSoup(response.text, 'html.parser')

    def get_information(self, disease_page: BeautifulSoup) -> str:
        overview = disease_page.find(string='Overview').parent
        information = []
        current = overview.find_next_sibling()

        while 'acces-list-container' not in (current.get('class') if current.get('class') else []):
            if current.text != '':
                information.append(current.text)
            current = current.find_next_sibling()

        return '\n'.join(information)

    def get_symptoms(self, disease_page: BeautifulSoup) -> list[str]:
        symptoms = disease_page.find(string='Symptoms', name='h2')

        while symptoms.name != 'ul':
            symptoms = symptoms.find_next_sibling() 
    
        return [symptom.text for symptom in symptoms.findAll(name='li')]

    def get_remedies(self, disease_page: BeautifulSoup) -> list[str]:
        pass


scraper = DiseaseInfoScraper([])
print(scraper.get_disease('dengue'))