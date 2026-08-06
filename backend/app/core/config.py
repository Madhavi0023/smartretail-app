from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SmartRetail API"
    APP_ENV: str = "development"
    APP_PORT: int = 8000

    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "smartretail"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    REDIS_URL: str = "redis://redis:6379"

    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()