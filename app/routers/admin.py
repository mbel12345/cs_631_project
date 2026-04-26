from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_admin_user
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')

@router.get('/admin/home')
def home(
    request: Request,
    user = Depends(get_current_admin_user),
):

    return templates.TemplateResponse(
        'admin/index.html',
        {
            'request': request,
        },
    )

@router.get('/admin/new-reservation')
def new_reservation_form(
    request: Request,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):

    customers = db.execute(
        text('''
            SELECT
                Customer_Name AS name,
                Customer_Address AS address
            FROM
                Customer
            ORDER BY
                name ASC,
                address ASC
        ''')
    ).fetchall()

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
            'first_name': user['first_name'],
            'customers': customers,
            'locations': locations,
            'car_classes': car_classes,
        },
    )

@router.post('/admin/new-reservation')
async def new_reservation(
    request: Request,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):

    form = await request.form()

    customer_name = (form['customer'].split('~')[0]).strip()
    customer_address = '~'.join(form['customer'].split('~')[1:]).strip()
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

        return RedirectResponse('/admin/new-reservation?success=1', status_code=303)

    except IntegrityError as e:

        print(e)
        db.rollback()
        return RedirectResponse('/admin/new-reservation?exists=1', status_code=303)

    except Exception as e:

        print(e)
        db.rollback()
        return RedirectResponse('/admin/new-reservation?error=1', status_code=303)

@router.get('/admin/reservations')
def reservation_page(
    request: Request,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):

    reservations = db.execute(
        text('''
            SELECT
                R.Customer_Name,
                R.Pickup_Location_ID,
                TO_CHAR(R.Pickup_Date_Time, 'YYYY-MM-DD HH24:MI') AS pickup_time,
                TO_CHAR(R.Return_Date_Time, 'YYYY-MM-DD HH24:MI') AS return_time,
                R.Customer_Address,
                C.Contract_Number,
                C.VIN,
                TO_CHAR(C.Start_Date_Time, 'YYYY-MM-DD HH24:MI') AS start_time,
                C.Start_Odometer_Reading,
                TO_CHAR(C.End_Date_Time, 'YYYY-MM-DD HH24:MI') AS end_time,
                C.End_Odometer_Reading,
                C.License_State,
                C.License_Number,
                C.License_Expiry_Month,
                C.License_Expiry_Year,
                C.Credit_Card_Type,
                C.Credit_Card_Number,
                C.Credit_Card_Expiry_Month,
                C.Credit_Card_Expiry_Year,
                C.Total_Cost
            FROM Reservation AS R
            JOIN Rental_Agreement AS C ON
                R.Customer_Name = C.Customer_Name AND
                R.Customer_Address = C.Customer_Address AND
                R.Pickup_Location_ID = C.Pickup_Location_ID AND
                R.Pickup_Date_Time = C.Pickup_Date_Time
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
            'headers': reservations[0].keys() if len(reservations) > 0 else [],
            'reservations': reservations,
        },
    )

@router.get('/admin/users')
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
        'admin/user_list.html',
        {
            'request': request,
            'users': users,
        },
    )
