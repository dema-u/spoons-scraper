from typing import List

from pydantic import SecretStr
import psycopg2

from spoons_scraper.types import SpoonsLocation
from spoons_scraper.settings import Settings
from spoons_scraper.postgres.queries import QUERIES_PATH


class PostgresClient:
    
    def __init__(self, host: str, port: str, user: str, password: SecretStr, db_name: str):
        self._connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=db_name
        )

    def save_locations(self, locations: List[SpoonsLocation]):
        cursor = self._connection.cursor()
        
        insert_input = [
            (
                location.pub_name,
                location.street_address,
                location.locality,
                location.region,
                location.post_code
            )
            for location in locations
        ]
        
        cursor.executemany(self.get_query('save_locations'), insert_input)
        
        self._connection.commit()
        cursor.close()
        
    def get_all_locations(self) -> List[SpoonsLocation]:
        cursor = self._connection.cursor()
        
        cursor.execute(self.get_query('get_locations'))
        
        locations = [
            SpoonsLocation(
                pub_name=pub_name,
                street_address=street_address,
                locality=locality,
                region=region,
                post_code=post_code
            )
            for pub_name, street_address, locality, region, post_code
            in cursor.fetchall()
        ]
        
        cursor.close()
        return locations

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
