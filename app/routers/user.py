from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

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
