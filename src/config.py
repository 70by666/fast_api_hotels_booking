from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DB_NAME_TEST: str

    SECRET_AUTH: str
    ALGORITHM: str

    REDIS: str

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASS: str

    class Config:
        env_file = '.env'


settings = Settings()
