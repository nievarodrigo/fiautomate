from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./fiautomate.db"
    MP_ACCESS_TOKEN: str = ""
    MP_WEBHOOK_SECRET: str = ""
    ALLOWED_NUMBERS: str = ""  # números autorizados a enviar comandos, separados por coma

    class Config:
        env_file = ".env"


settings = Settings()
