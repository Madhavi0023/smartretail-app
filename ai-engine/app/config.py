import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """Application configuration loaded from environment variables."""

    # ==================================================
    # Kubernetes
    # ==================================================

    KUBERNETES_NAMESPACE = os.getenv(
        "KUBERNETES_NAMESPACE",
        "default",
    )

    # ==================================================
    # Ollama / AI
    # ==================================================

    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434",
    )

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "qwen2.5:0.5b",
    )

    # ==================================================
    # Jira
    # ==================================================

    JIRA_URL = os.getenv("JIRA_URL")
    JIRA_EMAIL = os.getenv("JIRA_EMAIL")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

    # ==================================================
    # Email / SMTP
    # ==================================================

    SMTP_HOST = os.getenv(
        "SMTP_HOST",
        "smtp.gmail.com",
    )

    SMTP_PORT = int(
        os.getenv(
            "SMTP_PORT",
            "587",
        )
    )

    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    NOTIFICATION_EMAIL = os.getenv(
        "NOTIFICATION_EMAIL"
    )


settings = Settings()