from pydantic import BaseSettings, Field, SecretStr


class Settings:
    
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'root'
    DB_PASS: SecretStr = 'root'
    DB_NAME: str = 'spoons'
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        