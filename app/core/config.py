# Config file
from pydantic_settings import BaseSettings,SettingsConfigDict
import os
import dotenv
from functools import lru_cache

dotenv.load_dotenv()

class Settings(BaseSettings):
    DB_USER: str 
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str


    REDIS_URL: str 
    SCRAPE_TIME: str
    
    PHONE_NUMBER_ID: str
    VERIFY_TOKEN: str
    WHATSAPP_TOKEN: str

    TOKEN_SUNAT_API: str

    

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
