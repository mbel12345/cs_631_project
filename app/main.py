from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import get_engine
from app.database.database_init import init_db
from app.routers.admin import router as admin_router
from app.routers.login import router as login_router
from app.routers.user import router as user_router

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

app.include_router(login_router)
app.include_router(user_router)
app.include_router(admin_router)
