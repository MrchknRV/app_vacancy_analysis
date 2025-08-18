from dataclasses import dataclass


@dataclass
class Employer:
    """Класс для представления работодателя"""
    id: int
    name: str
    url: str
    open_vacancies: int


@dataclass
class Vacancy:
    """Класс для представления вакансии"""
    id: int
    employer_id: int
    title: str
    salary_from: int | None
    salary_to: int | None
    currency: str | None
    url: str