from pydantic import BaseSettings, Field, HttpUrl


class Settings(BaseSettings):

    DB_HOST: str = Field("localhost")
    DB_PORT: int = Field(5432)
    DB_USER: str = Field("root")
    DB_PASS: str = Field("root")
    DB_NAME: str = Field("spoons")

    SPOONS_BASE_URL: HttpUrl = Field("https://www.jdwetherspoon.com")
    SPOONS_LOCATIONS_PATH: str = Field("/site-map")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
