from config import EMPLOYER_IDS
from src.DBCreator import DBCreator
from src.DBManager import DBManager
from src.HH import HeadHunterAPI


def main():
    db_creator = DBCreator()
    db_creator.create_database()
    db_creator.create_tables()
    hh_api = HeadHunterAPI()
    db_manager = DBManager()

    print("Получение данных о компаниях...")
    employers = hh_api.get_employers(EMPLOYER_IDS)
    db_manager.insert_employers(employers)

    print("Получение данных о вакансиях...")
    for employer_id in EMPLOYER_IDS:
        vacancies = hh_api.get_vacancies(employer_id)
        db_manager.insert_vacancies(vacancies)

    print("Данные успешно загружены в базу данных")

    while True:
        print("\nВыберите действие:")
        print("1. Список компаний и количество вакансий")
        print("2. Список всех вакансий")
        print("3. Средняя зарплата по вакансиям")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("> ")

        if choice == "1":
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"{company['company']}: {company['vacancies_count']} вакансий")

        elif choice == "2":
            vacancies = db_manager.get_all_vacancies()
            for vacancy in vacancies:
                print(f"{vacancy['company']} - {vacancy['title']}")
                print(f"Зарплата: {vacancy['salary']}")
                print(f"Ссылка: {vacancy['url']}\n")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            print(f"Найдено {len(vacancies)} вакансий с зарплатой выше средней:")
            for vacancy in vacancies:
                print(f"{vacancy['company']} - {vacancy['title']}")
                print(f"Зарплата: {vacancy['salary']}")
                print(f"Ссылка: {vacancy['url']}\n")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print(f"Найдено {len(vacancies)} вакансий по запросу '{keyword}':")
            for vacancy in vacancies:
                print(f"{vacancy['company']} - {vacancy['title']}")
                print(f"Зарплата: {vacancy['salary']}")
                print(f"Ссылка: {vacancy['url']}\n")

        elif choice == "0":
            break

        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
