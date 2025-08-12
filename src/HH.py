import requests

from src.BaseClasses import HHBase


class HH(HHBase):
    """
    Класс для работы с API HeadHunter
    """

    __slots__ = ("__url", "__headers", "__params", "__vacancies")
    __url: str
    __headers: dict
    __params: dict
    __vacancies: list

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []
        super().__init__()

    def load_vacancies(self, keyword: str):
        """Получение данных от сервера"""
        self.__params["text"] = keyword
        while self.__params.get("page") != 2:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1
        return self.__vacancies
