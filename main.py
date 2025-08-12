import os

from dotenv import load_dotenv

from src.DBManager import DBManager
from src.FileHandlerJob import FileHandlerJob
from src.HH import HH
from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.Vacancy import Vacancy

load_dotenv()

hh_api = HH()

DB_NAME = os.getenv("DATABASE_NAME") or ""
DB_PASSWORD = os.getenv("DATABASE_PASSWORD") or ""
DB_USER = os.getenv("DATABASE_USER") or ""
DB_HOST = os.getenv("DATABASE_HOST") or ""
DB_PORT = os.getenv("DATABASE_PORT") or ""
db_manager = DBManager(DB_NAME, DB_PASSWORD, DB_USER, DB_HOST, DB_PORT)

file_handler = FileHandlerJob()
db_manager.create_database()
db_manager.connect()
db_manager.create_table()

count_vacancies = db_manager.get_companies_and_vacancies_count()
get_all_vacancies = db_manager.get_all_vacancies()
get_avg_salary = db_manager.get_avg_salary()
get_vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
get_vacancies_with_keyword = db_manager.get_vacancies_with_keyword("python")
print(count_vacancies)
print(get_all_vacancies)
print(get_avg_salary)
print(get_vacancies_with_higher_salary)
print(get_vacancies_with_keyword)


def main():
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")

    hh_vacancies = hh_api.load_vacancies(search_query)
    vacancies_list = Vacancy.create_vacancies(hh_vacancies)
    db_manager.insert_vacancies(vacancies_list)
    file_handler.add_vacancy(vacancies_list)

    file_handler.delete_vacancy(vacancies_list[0])
    db_manager.delete_vacancy(vacancies_list[0])
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    main()
