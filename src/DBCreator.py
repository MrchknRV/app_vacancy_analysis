import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


class DBCreator:
    """Класс для создания БД и таблиц"""

    def __init__(self):
        self.default_conn_params = {
            "dbname": "postgres",
            "user": DB_USER,
            "password": DB_PASSWORD,
            "host": DB_HOST,
            "port": DB_PORT,
        }
        self.conn_params = {
            "dbname": DB_NAME,
            "user": DB_USER,
            "password": DB_PASSWORD,
            "host": DB_HOST,
            "port": DB_PORT,
            "client_encoding": "utf8",
        }

    def create_database(self):
        """Создание базы данных"""
        try:
            conn = psycopg2.connect(**self.default_conn_params)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}").format(sql.Literal(DB_NAME)))
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(sql.SQL("CREATE DATABASE {} WITH ENCODING 'UTF8'").format(sql.Identifier(DB_NAME)))
                print(f"База данных {DB_NAME} успешно создана")
            else:
                print(f"База данных {DB_NAME} уже существует")

            cursor.close()
            conn.close()
        except Exception as exc:
            print(f"Ошибка при создании базы данных: {exc}")

    def create_tables(self):
        """Создание таблиц в базе данных"""
        try:
            conn = psycopg2.connect(**self.conn_params)
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS employers (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(255),
                    open_vacancies INTEGER
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    id INTEGER PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(id),
                    title VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency VARCHAR(10),
                    url VARCHAR(255)
                )
            """
            )

            conn.commit()
            print("Таблицы успешно созданы")

            cursor.close()
            conn.close()
        except Exception as exc:
            print(f"Ошибка при создании таблиц: {exc}")
