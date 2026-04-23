import logging

from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_engine(database_url: str = SQLALCHEMY_DATABASE_URL):

    # Factory function to create a new SQLAlchemy engine.

    return create_engine(database_url)

def get_sessionmaker(engine):

    # Factory function to create new sessionmaker

    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
1
@contextmanager
def managed_db_session():

    # Context manager for safe database session handling
    session = SessionLocal()
    try:
        yield session
    except SQLAlchemyError as e:
        logger.error(f'Database error: {str(e)}')
        raise
    finally:
        session.close()

def query_file(file_name: str):

    logger.info(f'query_file({file_name})')
    with managed_db_session() as db:
        with open(file_name, 'r') as in_file:
            stmt = ''
            for line in in_file:
                if line.strip().startswith('--') or not line.strip():
                    continue

                stmt += line

                if stmt.strip().endswith(';'):
                    logger.info(stmt)
                    db.execute(text(stmt))
                    stmt = ''
            db.commit()
