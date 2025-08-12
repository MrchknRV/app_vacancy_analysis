from abc import ABC, abstractmethod


class BaseDBManager(ABC):
    """Абстрактный метод для всех классов подключений к БД"""

    @abstractmethod
    def connect(self): ...

    @abstractmethod
    def get_companies_and_vacancies_count(self): ...

    @abstractmethod
    def get_all_vacancies(self): ...

    @abstractmethod
    def get_avg_salary(self): ...

    @abstractmethod
    def get_vacancies_with_higher_salary(self): ...

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str): ...

    @abstractmethod
    def create_database(self): ...

    @abstractmethod
    def create_table(self): ...

    @abstractmethod
    def insert_company(self, company_id: int, company_name: str): ...

    @abstractmethod
    def insert_vacancies(self, vacancies): ...


class BaseVacancy(ABC):
    """Абстрактный класс"""

    @staticmethod
    @abstractmethod
    def create_vacancies(list_hh_vacancy: list): ...

    @abstractmethod
    def to_dict(self): ...


class FileHandlerBase(ABC):
    """Абстрактный класс который перечисляет методы наследоваемых классов"""

    @abstractmethod
    def write(self, text: list[dict], file_mode: str): ...

    @abstractmethod
    def open_file(self): ...

    @abstractmethod
    def add_vacancy(self, list_vacancy_hh: list): ...

    @abstractmethod
    def delete_vacancy(self, vacancy): ...


class HHBase(ABC):
    """Абстрактный класс"""

    @abstractmethod
    def load_vacancies(self, keyword: str): ...
