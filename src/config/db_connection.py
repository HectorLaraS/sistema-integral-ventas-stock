import psycopg
from src.config.settings import settings


class DBConnection:
    def get_conn(self):
        return psycopg.connect(
            host=settings.DB_HOST,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=settings.DB_PORT
        )