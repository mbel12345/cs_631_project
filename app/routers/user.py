from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.auth.jwt import AuthError
from app.auth.jwt import get_current_user
from app.auth.jwt import get_current_user_optional
from app.database import get_db
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')

@router.get('/')
def home_page(
    request: Request,
    user = Depends(get_current_user_optional),
):

    
    return templates.TemplateResponse(
        'user/index.html',
        {
            'request': request,
            'user': user['first_name'] if user is not None else None,
            'first_name': user['first_name'] if user is not None else None,
            'last_name': user['last_name'] if user is not None else None
        },
    )


@router.get('/user/home')
def home(
    request: Request,
    user = Depends(get_current_user_optional),
):

    return templates.TemplateResponse(
        'user/index.html',
        {
            'request': request,
            'user': user['first_name'] if user is not None else None,
            'first_name': user['first_name'] if user is not None else None,
            'last_name': user['last_name'] if user is not None else None
        },
    )

@router.get('/user/reservations')
def reservation_page(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
    location: Optional[str] = None,
    pickup_start: Optional[str] = None,
    pickup_end: Optional[str] = None,
    
):
    conditions = [
        '1 = 1',
    ]

    conditions.append(f"LOWER(R.Customer_Name) LIKE '%{user['customer_name'].lower()}%'")
    conditions.append(f"LOWER(R.Customer_Address) LIKE '%{user['address'].lower()}%'")

    if location and location.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(R.Pickup_Location_ID) LIKE '%{location.lower()}%'")

    if pickup_start and pickup_start.lower() not in ('none', 'null', ''):
        conditions.append(f"R.Pickup_Date_Time >= '{pickup_start}'")

    if pickup_end and pickup_end.lower() not in ('none', 'null', ''):
        conditions.append(f"R.Pickup_Date_Time <= '{pickup_end}'")
    
    

    reservations = db.execute(
        text(f'''
            SELECT
                R.Customer_Name,
                R.Pickup_Location_ID,
                TO_CHAR(R.Pickup_Date_Time, 'YYYY-MM-DD HH24:MI') AS pickup_time,
                TO_CHAR(R.Return_Date_Time, 'YYYY-MM-DD HH24:MI') AS return_time,
                R.Customer_Address               
            FROM Reservation AS R
            WHERE
                {' AND '.join(conditions)}
            ORDER BY
                R.Pickup_Date_Time DESC,
                R.Customer_Name ASC
        '''
        )
    ).fetchall()

    reservations = [dict(r._mapping) for r in reservations]

    return templates.TemplateResponse(
        'user/reservation_list.html',
        {
            'request': request,
            'user': user,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'headers': reservations[0].keys() if len(reservations) > 0 else [],
            'reservations': reservations,
        },
    )

@router.get('/user/new-reservation')
def new_user_reservation_form(
    request: Request,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locations = db.execute(
        text('''
            SELECT
                Location_ID AS location_id,
                Address AS address
            FROM
                Location
            ORDER BY
                Location_ID ASC
        ''')
    ).fetchall()

    car_classes = db.execute(
        text('''
            SELECT
                Class_Name AS car_class
            FROM
                Car_Class
            ORDER BY
                car_class ASC
        ''')
    ).fetchall()

    car_classes = [c[0] for c in car_classes]

    return templates.TemplateResponse(
        'user/new_reservation.html',
        {
            'request': request,
            'user': user,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'locations': locations,
            'car_classes': car_classes,
        },
    )


@router.post('/user/new-reservation')
async def new_user_reservation(
    request: Request,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    form = await request.form()
   
    customer_name = user['customer_name'].strip()
    customer_address = user['address'].strip()
    pickup_location_id = (form['pickup_location_id'].split('~')[0]).strip()
    class_name = form['class_name'].strip()
    pickup_date_time = form['pickup_date_time'].strip()
    return_date_time = form['return_date_time'].strip()

    try:
        db.execute(text('''
            INSERT INTO Reservation (Customer_Name, Customer_Address, Pickup_Location_ID, Class_Name, Pickup_Date_Time, Return_Date_Time)
            VALUES (:customer_name, :customer_address, :pickup_location_id, :class_name, :pickup_date_time, :return_date_time)'''),
            {
                'customer_name': customer_name,
                'customer_address': customer_address,
                'pickup_location_id': pickup_location_id,
                'class_name': class_name,
                'pickup_date_time': pickup_date_time,
                'return_date_time': return_date_time,
            },
        )

        db.commit()

        return RedirectResponse('/user/new-reservation?success=1', status_code=303)

    except IntegrityError as e:

        print(e)
        db.rollback()
        return RedirectResponse('/user/new-reservation?exists=1', status_code=303)

    except Exception as e:

        print(e)
        db.rollback()
        return RedirectResponse('/user/new-reservation?error=1', status_code=303)


@router.get('/user/info')
def user_info(
    request: Request,
    user = Depends(get_current_user)
):

    return templates.TemplateResponse(
        '/user/user_info.html',
        {
            'request': request,
            'user': user,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
        },
    )

