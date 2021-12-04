from typing import List

from pydantic import SecretStr
import psycopg2

from spoons_scraper.types import SpoonsLocation
from spoons_scraper.settings import Settings
from spoons_scraper.postgres.queries import QUERIES_PATH


class PostgresClient:
    
    def __init__(self, host: str, port: str, user: str, password: SecretStr, db_name: str):
        self._client = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=db_name
        )

    def save_locations(self, locations: List[SpoonsLocation]):
        pass
        
    def get_all_locations(self) -> List[SpoonsLocation]:
        pass

    @staticmethod
    def get_query(query_name: str) -> str:
        with open(QUERIES_PATH / f'{query_name}.sql', 'r') as file:
            return file.read()
            
    @classmethod
    def bootstrap_from_settings(cls):
        settings = Settings()
        return cls(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            db_name=settings.DB_NAME
        )   
        
        