from pydantic_settings import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str
    db_async_connection_str: str
    test_db_async_connection_str: str

load_dotenv()
settings = Settings()