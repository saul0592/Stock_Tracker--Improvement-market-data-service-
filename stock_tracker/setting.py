# settings.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() # Carga el archivo .env

class Settings(BaseSettings):
    # Definimos que esta variable debe existir
    ALPHA_VANTAGE_API_KEY : str

settings = Settings()