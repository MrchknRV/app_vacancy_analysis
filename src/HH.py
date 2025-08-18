import requests
from src.Models import Employer, Vacancy


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.base_url = "https://api.hh.ru/"

    def get_employers(self, employer_ids: list) -> list:
        """Получение данных о компаниях по их ID"""
        employers = []
        for employer_id in employer_ids:
            url = f"{self.base_url}employers/{employer_id}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                employer = Employer(
                    id=data['id'],
                    name=data['name'],
                    url=data['alternate_url'],
                    open_vacancies=data['open_vacancies']
                )
                employers.append(employer)
        return employers

    def get_vacancies(self, employer_id: int) -> list:
        """Получение вакансий компании"""
        url = f"{self.base_url}vacancies?employer_id={employer_id}"
        response = requests.get(url)
        vacancies = []
        if response.status_code == 200:
            data = response.json()
            for item in data['items']:
                salary = self._parse_salary(item.get('salary'))
                vacancy = Vacancy(
                    id=item['id'],
                    employer_id=employer_id,
                    title=item['name'],
                    salary_from=salary['from'],
                    salary_to=salary['to'],
                    currency=salary['currency'],
                    url=item['alternate_url']
                )
                vacancies.append(vacancy)
        return vacancies

    def _parse_salary(self, salary: dict) -> dict:
        """Обработка данных о зарплате"""
        if not salary:
            return {'from': None, 'to': None, 'currency': None}
        return {
            'from': salary.get('from'),
            'to': salary.get('to'),
            'currency': salary.get('currency')
        }
