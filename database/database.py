import os
import sys

from dotenv import load_dotenv

from sqlalchemy import inspect
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists

from database.models import Base
from core.services.debug_service.logger_config import get_logger

logger = get_logger(__name__)

load_dotenv()

POSTGRES_USER = os.getenv("DB_USER")
POSTGRES_PASSWORD = os.getenv("DB_PASSWORD")
POSTGRES_SERVER = os.getenv("DB_HOST")
POSTGRES_PORT = os.getenv("DB_PORT")
POSTGRES_DB = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def is_database_exist():
    return database_exists(DATABASE_URL)


def get_db_session():
    session_maker = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    return session_maker()


def init_db():
    logger.info(f"Connecting to: {POSTGRES_DB} on {POSTGRES_SERVER}...")

    try:
        if is_database_exist() is False:
            logger.error("Can not connect to database")
            return False
        logger.info("Database connection OK.")

        inspector = inspect(engine)
        existing_tables = set(inspector.get_table_names())

        expected_tables = set(Base.metadata.tables.keys())
        missing_tables = expected_tables - existing_tables

        if not missing_tables:
            logger.info("All expected tables already exist in the database.")
            logger.info(f"Existing tables: {sorted(existing_tables)}")
            return True

        logger.info(f"Missing tables detected, creating: {sorted(missing_tables)}")
        Base.metadata.create_all(bind=engine)
        logger.info(f"Created: {sorted(missing_tables)}")

        inspector_after = inspect(engine)
        existing_after = set(inspector_after.get_table_names())
        still_missing = expected_tables - existing_after

        if still_missing:
            logger.error(f"Some tables could NOT be created: {sorted(still_missing)}")
            return False

        logger.info(f"All tables in database: {sorted(existing_after)}")
        return True

    except Exception as e:
        logger.error(f"Error during DB initialization: {e}")
        sys.exit(1)
