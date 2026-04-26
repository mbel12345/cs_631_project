from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.jwt import create_token

router = APIRouter()
templates = Jinja2Templates(directory='app/templates/login')

@router.get('/login')
def reservation_page(request: Request):

    return templates.TemplateResponse(
        'login.html',
        {
            'request': request,
        },
    )

@router.post('/login')
async def login(request: Request, db: Session = Depends(get_db)):

    form = await request.form()

    username = form['login-username'].strip()
    password = form['login-password'].strip()

    if not username or not password:
        return RedirectResponse('/login?bad-login=1', status_code=303)

    user = db.execute(text('SELECT * FROM Users WHERE username = :username AND password = :password'), {
        'username': username,
        'password': password,
    }).fetchone()

    if user is None:
        return RedirectResponse('/login?bad-login=1', status_code=303)

    user = dict(user._mapping)

    redirect_location = '/admin/reservations' if user['is_admin'] is True else '/user/new-reservation'
    access_token = create_token(user['username'])
    response = RedirectResponse(redirect_location, status_code=303)
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=False,
        samesite='lax',
    )

    return response

@router.get('/logout')
def logout():

    response = RedirectResponse('/login', status_code=303)
    response.delete_cookie('access_token')
    return response

@router.post('/register')
async def register(request: Request, db: Session = Depends(get_db)):

    form = await request.form()

    username = form['username'].strip()
    password = form['password'].strip()
    confirm_password = form['confirm_password'].strip()
    customer_name = f"{form['first_name']} {form['last_name']}".strip()
    customer_address = form['address'].strip()

    if confirm_password != password:
        return RedirectResponse('/login?password_mismatch=1', status_code=303)

    try:
        db.execute(text('INSERT INTO Customer (Customer_Name, Customer_Address) VALUES (:customer_name, :customer_address)'), {
            'customer_name': customer_name,
            'customer_address': customer_address,
        })

        db.execute(text('INSERT INTO Users (Username, Password, Customer_Name, Customer_Address) VALUES (:username, :password, :customer_name, :customer_address)'), {
            'username': username,
            'password': password,
            'customer_name': customer_name,
            'customer_address': customer_address,
        })

        db.commit()

        return RedirectResponse('/login?registered=1', status_code=303)

    except IntegrityError as e:

        print(e)
        db.rollback()
        return RedirectResponse('/login?exists=1', status_code=303)

    except Exception as e:

        print(e)
        db.rollback()
        return RedirectResponse('/login?error=1', status_code=303)
