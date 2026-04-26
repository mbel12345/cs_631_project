from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # Database settings
    DATABASE_URL: str = 'postgresql://postgres:postgres@localhost:5432/car_rental'

    # JWT settings
    JWT_SECRET_KEY: str = 'super-secret-key-asdfasdfadfsafdasdfsadf'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Security settings
    BCRYPT_ROUNDS: int = 12

settings = Settings()
