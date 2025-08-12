import psycopg2
from psycopg2.extensions import connection as PG_conn

from src.BaseClasses import BaseDBManager
from src.Vacancy import Vacancy


class DBManager(BaseDBManager):
    """Класс работы с БД PostgreSQL"""

    __slots__ = "conn", "dbname", "password", "user", "host", "port"

    def __init__(
        self, dbname: str, password: str, user: str = "postgres", host: str = "localhost", port: str = "5432"
    ):
        self.conn: PG_conn
        self.dbname = dbname
        self.password = password
        self.user = user
        self.host = host
        self.port = port

    def connect(self):
        """Соединение с БД"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port
            )
        except Exception as exc:
            raise ConnectionError(f"Ошибка подключения к БД: {exc}")

    def create_database(self):
        """Создание базы данных"""
        tmp_database = psycopg2.connect(
            dbname="template1", user=self.user, password=self.password, host=self.host, port=self.port
        )
        tmp_database.set_session(autocommit=True)
        cursor = tmp_database.cursor()
        cursor.execute(
            f"""
                SELECT 
                    COUNT(*)
                WHERE NOT EXISTS 
                (
                    SELECT FROM 
                        pg_database 
                    WHERE 
                        datname = '{self.dbname}'
                );
            """
        )
        chk_database = cursor.fetchone()
        if chk_database:
            if chk_database[0] == 1:
                cursor.execute(f"CREATE DATABASE {self.dbname};")
        cursor.close()

    def create_table(self):
        """Создание таблиц в БД"""
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS companies 
            (
                id INT PRIMARY KEY,
                name TEXT NOT NULL
            );
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies 
            (
                id_vacancy INT PRIMARY KEY,
                company_id INT REFERENCES companies(id) NOT NULL,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                salary_from INT,
                salary_to INT,
                requirement TEXT 
            );
        """
        )
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 
                c.name, COUNT(v) as count_v 
            FROM 
                companies as c 
            JOIN vacancies as v ON c.id = v.company_id 
            GROUP BY c.name 
            ORDER BY count_v DESC
            """
        )
        return cursor.fetchall()

    def delete_vacancy(self, vacancy: Vacancy):
        """Удаляет выбранную вакансию"""
        cursor = self.conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM 
                vacancy 
            WHERE 
                id_vacancy = '{vacancy.id_vacancy}'
            """
        )

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
        SELECT 
            c.name, v.name, v.salary_from || ' - ' || v.salary_to as salary, v.url  
        FROM 
            companies as c 
        JOIN 
            vacancies as v ON c.id = v.company_id 
        GROUP BY 
            c.name, v.name, v.salary_from, v.salary_to, v.url 
        """
        )
        return cursor.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 
                (AVG(salary_to) + AVG(salary_from)) / 2 as avg_salary 
            FROM 
                vacancies 
            WHERE 
                salary_to > 0 
            AND 
                salary_from > 0
            """
        )
        result = cursor.fetchone()
        if result:
            return int(result[0])
        cursor.close()
        return None

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        cursor = self.conn.cursor()
        cursor.execute(
            f"""
            SELECT 
                * 
            FROM 
                vacancies 
            WHERE 
                salary_to > {avg_salary}
        """
        )
        result = cursor.fetchall()
        if result:
            return result
        cursor.close()
        return None

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        cursor = self.conn.cursor()
        cursor.execute(
            f"""
            SELECT 
                * 
            FROM 
                vacancies
            WHERE 
                name iLIKE '%{keyword}%'
            """
        )
        result = cursor.fetchall()
        if result:
            return result
        cursor.close()
        return None

    def insert_company(self, company_id: int, company_name: str):
        """Вставка компании если она не существует в БД"""
        cursor = self.conn.cursor()
        cursor.execute(
            f"""
                SELECT 
                    COUNT(*) 
                FROM
                     companies
                WHERE  
                    id = {company_id}
            """
        )
        get_count = cursor.fetchone()
        if get_count and get_count[0] == 0:
            cursor.execute(
                """
            INSERT INTO companies 
                (id, name)
            VALUES 
                (%s, %s) 
            RETURNING 
                id
            """,
                [company_id, company_name],
            )
            result = cursor.fetchone()
            if result:
                company_id = int(result[0])
            else:
                return None

        return company_id

    def insert_vacancies(self, vacancies: list[Vacancy]):
        """Вставка вакансии в БД"""
        for vacancy in vacancies:
            cursor = self.conn.cursor()
            company_id = self.insert_company(vacancy.company_id, vacancy.company_name)
            cursor.execute(
                f"""
                SELECT COUNT(*) 
                FROM
                     vacancies
                WHERE  
                    id_vacancy = {vacancy.id_vacancy}
            """
            )
            get_count = cursor.fetchone()
            if get_count and get_count[0] == 0:
                cursor.execute(
                    f"""
                INSERT INTO vacancies 
                (
                    id_vacancy,
                    company_id,
                    name,
                    url,
                    salary_from,
                    salary_to,
                    requirement
                )
                VALUES 
                (
                    {vacancy.id_vacancy},   {company_id},
                    '{vacancy.name}',         '{vacancy.url}', 
                    {vacancy.salary_from},  {vacancy.salary_to}, 
                    '{vacancy.requirement}'
                )
                """
                )
                self.conn.commit()
