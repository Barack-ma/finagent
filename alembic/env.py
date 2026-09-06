import os

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from app.core.database import Base
from app.models.customer import CustomerModel


load_dotenv()

config = context.config

database_url = os.getenv("DATABASE_URL")

if database_url is None:
    raise RuntimeError("DATABASE_URL environment variable is not set")

config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata