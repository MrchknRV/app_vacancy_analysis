import re
from src.Vacancy import Vacancy


def filter_vacancies(vacancy_list: list[Vacancy], filter_words: list[str]) -> list[Vacancy]:
    """Фильтрация данных"""
    return [
        vacancy_data
        for vacancy_data in vacancy_list
        for find_text in filter_words
        if re.search(find_text, vacancy_data.name, re.I)
    ]


def get_vacancies_by_salary(filtered_vacancies: list[Vacancy], salary_range: str) -> list[Vacancy]:
    """Получение данных по ценам"""
    salary_from, salary_to = [float(salary.strip()) for salary in salary_range.split("-")]
    list_result = []
    for vacancy_data in filtered_vacancies:
        if salary_from <= vacancy_data.salary_from <= salary_to and salary_from <= vacancy_data.salary_to <= salary_to:
            list_result.append(vacancy_data)
    return list_result


def sort_vacancies(ranged_vacancies: list[Vacancy]) -> list[Vacancy]:
    """Сортировка данных"""
    return sorted(ranged_vacancies, reverse=True)


def get_top_vacancies(sorted_vacancies: list[Vacancy], top_n: int) -> list[Vacancy]:
    """Вывод ТОП данных по цене"""
    return sorted_vacancies[:top_n]


def print_vacancies(top_vacancies: list[Vacancy]) -> None:
    """Вывод данных в консоль"""
    for top_v in top_vacancies:
        print(top_v)
