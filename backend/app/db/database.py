# Database configuration will be added in the next sprint.
from sqlalchemy import create_engine

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)