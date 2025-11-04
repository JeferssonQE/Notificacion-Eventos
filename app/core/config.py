# Config file
from pydantic_settings import BaseSettings,SettingsConfigDict
import os
import dotenv
from functools import lru_cache

dotenv.load_dotenv()

class Settings(BaseSettings):
    DB_USER: str = None
    DB_PASSWORD: str = None
    DB_HOST: str = None
    DB_PORT: str = None
    DB_NAME: str = None


    REDIS_URL: str = None
    SCRAPE_TIME: str = None
    
    PHONE_NUMBER_ID: str = None
    VERIFY_TOKEN: str = None
    WHATSAPP_TOKEN: str = None

    TOKEN_SUNAT_API: str = None

    EMAIL_USER: str
    EMAIL_PASS: str
    EMAIL_TO: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
#cache        
@lru_cache()
def get_settings():
    return Settings()

settings = Settings()
