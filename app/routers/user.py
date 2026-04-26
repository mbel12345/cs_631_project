from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_user
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory='app/templates/user')

@router.get('/user/reservations')
def reservation_page(
    request: Request,
    db: Session = Depends(get_db)
):

    locations = db.execute(text('SELECT Location_ID, Address FROM Location ORDER BY Location_ID ASC')).mappings().all()

    return templates.TemplateResponse(
        'reservations.html',
        {
            'request': request,
            'locations': locations,
        },
    )

@router.get('/user/new-reservation')
def new_reservation(
    request: Request,
    user = Depends(get_current_user)
):

    return templates.TemplateResponse(
        'new_reservation.html',
        {
            'request': request,
            'customer_name': user['customer_name'],
        },
    )

@router.get('/user/info')
def new_reservation(
    request: Request,
    user = Depends(get_current_user)
):

    print(user)
    return templates.TemplateResponse(
        'user_info.html',
        {
            'request': request,
            'user': user,
        },
    )
