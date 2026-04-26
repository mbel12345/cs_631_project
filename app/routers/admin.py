from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_admin_user
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory='app/templates/admin')

@router.get('/admin/reservations')
def reservation_page(request: Request):

    return templates.TemplateResponse(
        'reservations.html',
        {
            'request': request,
        },
    )

@router.get('/admin/user-list')
def users_list(
    request: Request,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)):

    users = db.execute(
        text('''
            SELECT
                split_part(customer_name, ' ', 1) AS first_name,
                split_part(customer_name, ' ', 2) AS last_name,
                customer_address AS address,
                username,
                is_admin
            FROM Users
            ORDER BY last_name, first_name, address ASC
        '''
        )
    ).fetchall()
    return templates.TemplateResponse(
        'user_list.html',
        {
            'request': request,
            'users': users,
        },
    )
