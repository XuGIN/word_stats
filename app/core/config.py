from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MAX_FILE_SIZE_MB: int = 100
    TEMP_PATH: str = "temp"


    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

print(settings.MAX_FILE_SIZE_MB)