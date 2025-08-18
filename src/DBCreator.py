import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class DBCreator:
    """Класс для создания БД и таблиц"""

    def __init__(self):
        self.conn_params = {
            'dbname': DB_NAME,
            'user': DB_USER,
            'password': DB_PASSWORD,
            'host': DB_HOST,
            'port': DB_PORT
        }

    def create_database(self):
        """Создание базы данных"""
        try:
            conn = psycopg2.connect(**self.conn_params, client_encoding='utf8')
            conn.set_client_encoding('UTF8')
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", DB_NAME)
            exists = cursor.fetchone()

            if not exists:
                cursor.execute("CREATE DATABASE %s WITH ENCODING 'UTF8'", DB_NAME)
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
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                client_encoding='utf8'
            )
            conn.set_client_encoding('UTF8')
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(255),
                    open_vacancies INTEGER
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id INTEGER PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(id),
                    title VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency VARCHAR(10),
                    url VARCHAR(255))
            """)

            conn.commit()
            print("Таблицы успешно созданы")

            cursor.close()
            conn.close()
        except Exception as exc:
            print(f"Ошибка при создании таблиц: {exc}")
