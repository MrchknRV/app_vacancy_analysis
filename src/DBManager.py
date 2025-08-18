import psycopg2

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


class DBManager:
    """Класс для работы с данными в БД PostgreSQL"""

    def __init__(self):
        self.conn_params = {
            "dbname": DB_NAME,
            "user": DB_USER,
            "password": DB_PASSWORD,
            "host": DB_HOST,
            "port": DB_PORT,
        }

    def _connect(self):
        """Установка соединения с БД"""
        conn = psycopg2.connect(**self.conn_params)
        conn.set_client_encoding("UTF8")
        return conn

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании

        Returns:
            Список словарей с информацией о компаниях и количестве вакансий
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, COUNT(v.id) as vacancies_count
                    FROM employers e
                    LEFT JOIN vacancies v ON e.id = v.employer_id
                    GROUP BY e.name
                    ORDER BY vacancies_count DESC
                """
                )
                result = []
                for row in cur.fetchall():
                    result.append({"company": row[0], "vacancies_count": row[1]})
                return result

    def get_all_vacancies(self) -> list:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию

        Returns:
            Список словарей с информацией о вакансиях
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title, 
                           v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                """
                )
                result = []
                for row in cur.fetchall():
                    salary = self._format_salary(row[2], row[3], row[4])
                    result.append({"company": row[0], "title": row[1], "salary": salary, "url": row[5]})
                return result

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по вакансиям

        Returns:
            Средняя зарплата
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT AVG((salary_from + salary_to) / 2)
                    FROM vacancies
                    WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
                """
                )
                return round(float(cur.fetchone()[0]), 2)

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям

        Returns:
            Список вакансий с зарплатой выше средней
        """
        avg_salary = self.get_avg_salary()
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title, 
                           v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE (v.salary_from + v.salary_to) / 2 > %s
                """,
                    (avg_salary,),
                )
                result = []
                for row in cur.fetchall():
                    salary = self._format_salary(row[2], row[3], row[4])
                    result.append({"company": row[0], "title": row[1], "salary": salary, "url": row[5]})
                return result

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся переданные слова

        Args:
            keyword: Ключевое слово для поиска в названиях вакансий

        Returns:
            Список найденных вакансий
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title, 
                           v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE LOWER(v.title) LIKE %s
                """,
                    (f"%{keyword.lower()}%",),
                )
                result = []
                for row in cur.fetchall():
                    salary = self._format_salary(row[2], row[3], row[4])
                    result.append({"company": row[0], "title": row[1], "salary": salary, "url": row[5]})
                return result

    def _format_salary(self, salary_from: int, salary_to: int, currency: str) -> str:
        """
        Форматирует данные о зарплате в строку

        Args:
            salary_from: Нижняя граница зарплаты
            salary_to: Верхняя граница зарплаты
            currency: Валюта

        Returns:
            Отформатированная строка с зарплатой
        """
        if not salary_from and not salary_to:
            return "Не указана"

        parts = []
        if salary_from:
            parts.append(f"от {salary_from}")
        if salary_to:
            parts.append(f"до {salary_to}")
        if currency:
            parts.append(currency)

        return " ".join(parts)

    def insert_employers(self, employers: list) -> None:
        """Добавление работодателей в БД"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                for employer in employers:
                    cur.execute(
                        """
                        INSERT INTO employers (id, name, url, open_vacancies)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """,
                        (employer.id, employer.name, employer.url, employer.open_vacancies),
                    )
                conn.commit()

    def insert_vacancies(self, vacancies: list) -> None:
        """Добавление вакансий в БД"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                for vacancy in vacancies:
                    cur.execute(
                        """
                        INSERT INTO vacancies 
                        (id, employer_id, title, salary_from, salary_to, currency, url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """,
                        (
                            vacancy.id,
                            vacancy.employer_id,
                            vacancy.title,
                            vacancy.salary_from,
                            vacancy.salary_to,
                            vacancy.currency,
                            vacancy.url,
                        ),
                    )
                conn.commit()
