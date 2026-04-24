from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory='app/templates/user')

@router.get('/user/reservations')
def reservation_page(request: Request):

    return templates.TemplateResponse(
        'reservations.html',
        {
            'request': request,
        },
    )
