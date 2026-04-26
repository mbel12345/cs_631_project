import secrets
import uuid

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Union

from app.core.config import settings
from app.database import get_db

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
    bcrypt__rounds=settings.BCRYPT_ROUNDS,
)

def create_token(user_id: Union[str, uuid.UUID]) -> str:

    # Create a JWT token

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    if isinstance(user_id, uuid.UUID):
        user_id = str(user_id)

    to_encode = {
        'sub': user_id,
        'exp': expire,
        'iat': datetime.now(timezone.utc),
        'jti': secrets.token_hex(16),
    }

    secret = settings.JWT_SECRET_KEY
    try:
        return jwt.encode(to_encode, secret, algorithm=settings.ALGORITHM)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Could not create token: {str(e)}'
        )

def get_current_user(request: Request, db: Session = Depends(get_db)):

    # Get current user from the token and validate it. This dependency will be used by all the API calls.

    token = request.cookies.get('access_token')

    if not token:
        raise HTTPException(status_code=401, detail='Not authenticated')

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub')
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')

    if not username:
        raise HTTPException(status_code=401, detail='Invalid token payload')

    # Load user from DB
    result = db.execute(
        text('''
            SELECT
                username,
                split_part(customer_name, ' ', 1) AS first_name,
                split_part(customer_name, ' ', 2) AS last_name,
                customer_address AS address,
                is_admin
            FROM Users
            WHERE username = :username
        '''
        ),
        {
            'username': username,
        },
    ).fetchone()

    if result is None:
        raise HTTPException(status_code=401, detail='User not found')

    return dict(result._mapping)

def get_current_admin_user(request: Request, db: Session = Depends(get_db)):

    '''
    Get current user from the token and validate it.
    Fail if this user is not an admin.
    This dependency will be used by all the admin API calls.
    '''

    user = get_current_user(request, db)
    if user['is_admin'] is not True:
        raise HTTPException(status_code=401, detail='User is not an admin')

    return user
