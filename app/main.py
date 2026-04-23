from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import get_engine
from app.database.database_init import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):

    print('Creating tables...')
    engine = get_engine()
    init_db(engine=engine)
    print('Tables created successfully')
    yield

app = FastAPI(
    title='Car Rental API',
    description='API for car rental application',
    version='1.0.0',
    lifespan=lifespan,
    debug=True,
)

if __name__ == '__main__':

    import uvicorn
    uvicorn.run('app.main:app', host='127.0.0.1', port=8001, log_level='info')
