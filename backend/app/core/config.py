from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SmartRetail API"
    APP_ENV: str = "development"
    APP_PORT: int = 8000

    DATABASE_URL: str = "postgresql://username:password@localhost:5432/smartretail"
    REDIS_URL: str = "redis://localhost:6379"

    SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()