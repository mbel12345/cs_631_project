import traceback

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional
from uuid import uuid4

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
            'user': user['first_name'],
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

@router.get('/admin/new-rental')
def new_rental_form(
    request: Request,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):

    # Pull up all reservations that don't have a rental agreement

    reservations = db.execute(
        text('''
            SELECT
                R.Customer_Name AS customer_name,
                R.Customer_Address AS customer_address,
                R.Pickup_Location_ID AS pickup_location_id,
                TO_CHAR(R.Pickup_Date_Time, 'YYYY-MM-DD HH24:MI') as pickup_date_time
            FROM
                Reservation AS R
            LEFT OUTER JOIN Rental_Agreement AS C ON
                R.Customer_Name = C.Customer_Name AND
                R.Customer_Address = C.Customer_Address AND
                R.Pickup_Location_ID = C.Pickup_Location_ID AND
                R.Pickup_Date_Time = C.Pickup_Date_Time
            WHERE C.Contract_Number is NULL
            ORDER BY
                R.pickup_date_time DESC,
                R.customer_name ASC
        ''')
    ).fetchall()

    cars = db.execute(
        text('''
            SELECT
                C.VIN AS vin,
                C.Location_ID AS location_id,
                M.Car_Class AS car_class,
                M.Make AS make,
                M.Model AS model,
                M.Year_ AS year
            FROM
                Car AS C
            JOIN
                Car_Model AS M ON C.Model_ID = M.Model_ID
            ORDER BY
                Location_ID ASC,
                VIN ASC
        ''')
    ).fetchall()

    return templates.TemplateResponse(
        'user/new_rental.html',
        {
            'request': request,
            'first_name': user['first_name'],
            'reservations': reservations,
            'cars': cars,
        },
    )

@router.post('/admin/new-rental')
async def new_rental(
    request: Request,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):

    form = await request.form()

    customer_name = (form['reservation'].split('~')[0]).strip()
    customer_address = (form['reservation'].split('~')[1]).strip()
    pickup_location_id = (form['reservation'].split('~')[2]).strip()
    pickup_date_time = (form['reservation'].split('~')[3]).strip()
    vin = (form['vin'].split('~')[0]).strip()

    data = {
        'Customer_Name': customer_name,
        'Customer_Address': customer_address,
        'Pickup_Location_ID': pickup_location_id,
        'Pickup_Date_Time': pickup_date_time,
        'vin': vin,
        'Contract_Number': uuid4(),
    }

    for field in ['Start_Date_Time', 'End_Date_Time', 'Start_Odometer_Reading', 'End_Odometer_Reading', 'License_State', 'License_Number', 'License_Expiry_Month', 'License_Expiry_Year', 'Credit_Card_Type', 'Credit_Card_Number', 'Credit_Card_Expiry_Month', 'Credit_Card_Expiry_Year', 'Total_Cost']:

        value = form[field.lower()].strip()
        data[field] = value if value else None

    keys = list(data.keys())
    query = f"""
        INSERT INTO Rental_Agreement ({', '.join(keys)})
        VALUES ({', '.join(':' + k for k in keys)})
    """.strip()
    print(f'Insert Rental Query:\n{query}')
    try:
        db.execute(
            text(query),
            data,
        )

        db.commit()

        return RedirectResponse('/admin/new-rental?success=1', status_code=303)

    except IntegrityError as e:

        print(e)
        db.rollback()
        return RedirectResponse('/admin/new-rental?exists=1', status_code=303)

    except Exception as e:

        print(traceback.format_exc())
        db.rollback()
        return RedirectResponse('/admin/new-rental?error=1', status_code=303)

@router.get('/admin/reservations')
def reservation_page(
    request: Request,
    customer: Optional[str] = None,
    location: Optional[str] = None,
    pickup_start: Optional[str] = None,
    pickup_end: Optional[str] = None,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):

    conditions = [
        '1 = 1',
    ]

    if customer and customer.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(R.Customer_Name) LIKE '%{customer.lower()}%'")

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
