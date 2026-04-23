from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.database import Base
from app.database import get_engine

def init_db(engine: Engine) -> None:

    Base.metadata.create_all(bind=engine)

def drop_db(engine: Engine) -> None:

    Base.metadata.drop_all(bind=engine)

if __name__ == '__main__':

    engine = get_engine()
    drop_db(engine=engine)
    init_db(engine=engine)
