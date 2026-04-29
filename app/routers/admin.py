import traceback

from fastapi import APIRouter, Depends, HTTPException, Request
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

QUERIES = {
    "1": {
        "label": "NY customers having Multiple Reservations",
        "sql": """
            SELECT
                R.Customer_Name,
                R.Customer_Address,
                R.Pickup_Location_ID,
                COUNT(*)
            FROM Reservation AS R
            GROUP BY R.Customer_Name, R.Customer_Address, R.Pickup_Location_ID
            HAVING COUNT(*) > 1
            AND R.Customer_Address LIKE '%,%NY%'

        """,
    },
    "2": {
        "label": "Rank the cars by number of rentals",
        "sql": """
            SELECT
                M.Car_Class,
                COUNT(*) AS Rentals
            FROM rental_agreement AS A
            JOIN car AS C ON C.VIN = A.VIN
            JOIN car_model AS M ON M.Model_ID = C.Model_ID
            GROUP BY M.Car_Class
            ORDER BY COUNT(*) DESC, M.Car_Class ASC

        """,
    },
    "3": {
        "label": "Show all reservations that do not have a rental agreement",

        "sql": """
            SELECT
                R.*,
                A.Contract_Number
            FROM reservation AS R
            LEFT OUTER JOIN rental_agreement AS A ON
                A.Customer_Name = R.Customer_Name AND
                A.Customer_Address = R.Customer_Address AND
                A.Pickup_Location_ID = R.Pickup_Location_ID AND
                A.Pickup_Date_Time = R.Pickup_Date_Time
            WHERE
                A.Contract_Number IS NULL;


        """,
    },
    "4": {
        "label": "Select cars that have never been rented",
        "sql": """
            SELECT C.VIN
                FROM Car C
                WHERE NOT EXISTS (
                    SELECT *
                    FROM Rental_Agreement RA
                    WHERE RA.VIN = C.VIN
                );


        """,
    },
    "5": {
        "label": "Find customers whose reservation are all in ‘pending’ status",
        "sql": """
            SELECT DISTINCT R.Customer_Name, R.Customer_Address
            FROM Reservation R
            WHERE NOT EXISTS (
                SELECT *
                FROM Reservation R2
                WHERE R2.Customer_Name = R.Customer_Name
                AND R2.Customer_Address = R.Customer_Address
                AND (R2.Status_ IS NULL OR R2.Status_ <> 'pending')
            );


        """,
    },
    "6": {
        "label": "Find Customers who have never rented from Boston",
        "sql": """
            SELECT CU.Customer_Name, CU.Customer_Address
            FROM Customer CU
            WHERE NOT EXISTS (
                SELECT *
                FROM Rental_Agreement RA
                WHERE RA.Customer_Name = CU.Customer_Name
                AND RA.Customer_Address = CU.Customer_Address
                AND RA.Pickup_Location_ID = 'Boston Fast Rental'
            );


        """,
    },
    "7": {
        "label": "Find Customers who have rented every car at a location",
        "sql": """
            SELECT DISTINCT RA.Customer_Name, RA.Customer_Address
            FROM Rental_Agreement RA
            WHERE NOT EXISTS (
                SELECT *
                FROM Car C
                WHERE C.Location_ID = RA.Pickup_Location_ID
                AND NOT EXISTS (
                    SELECT *
                    FROM Rental_Agreement RA2
                    WHERE RA2.Customer_Name = RA.Customer_Name
                        AND RA2.Customer_Address = RA.Customer_Address
                        AND RA2.VIN = C.VIN
                )
            );


        """,
    },

    "8": {
        "label": "Find Customers whose every reservation was eventually turned into a rental agreement",
        "sql": """
            SELECT DISTINCT R.Customer_Name, R.Customer_Address
            FROM Reservation R
            WHERE NOT EXISTS (
                SELECT *
                FROM Reservation R2
                WHERE R2.Customer_Name = R.Customer_Name
                AND R2.Customer_Address = R.Customer_Address
                AND NOT EXISTS (
                    SELECT *
                    FROM Rental_Agreement RA
                    WHERE RA.Customer_Name = R2.Customer_Name
                        AND RA.Customer_Address = R2.Customer_Address
                        AND RA.Pickup_Date_Time = R2.Pickup_Date_Time
                )
            );



        """,
    },
}

@router.get('/admin/home')
def home(
    request: Request,
    user = Depends(get_current_admin_user),
):

    return templates.TemplateResponse(
        'admin/index.html',
        {
            'request': request,
            'user': user,
            'first_name': user['first_name'],
            'last_name': user['last_name']
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
        'admin/new_reservation.html',
        {
            'request': request,
            'user': user,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
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
        'admin/new_rental.html',
        {
            'request': request,
            'user': user,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
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
            LEFT JOIN Rental_Agreement AS C ON
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
    for row in reservations:
        for col in row:
            if row[col] is None:
                row[col] = ''

    return templates.TemplateResponse(
        'admin/reservation_list.html',
        {
            'request': request,
            'user': user,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'headers': reservations[0].keys() if len(reservations) > 0 else [],
            'reservations': reservations,
        },
    )

@router.get('/admin/cars')
def car_page(
    request: Request,
    vin: Optional[str] = None,
    location: Optional[str] = None,
    car_class: Optional[str] = None,
    make: Optional[str] = None,
    model: Optional[str] = None,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):

    conditions = [
        '1 = 1',
    ]

    if vin and vin.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(Car.VIN) LIKE '%{vin.lower()}%'")

    if location and location.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(Car.Location_ID) LIKE '%{location.lower()}%'")

    if car_class and car_class.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(Car_Class.Class_Name) LIKE '%{car_class.lower()}%'")

    if make and make.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(Car_Model.Make) LIKE '%{make.lower()}%'")

    if model and model.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(Car_model.Model) LIKE '%{model.lower()}%'")

    result = db.execute(
        text(f'''
            SELECT
                Car.VIN,
                Car.Location_ID,
                Car_Class.Class_Name,
                Car_Model.Make,
                Car_Model.Model,
                Car_Model.Year_,
                Car_Class.Daily_Rate,
                Car_Class.Weekly_Rate
            FROM Car
            JOIN Car_Model ON Car_Model.Model_ID = Car.Model_ID
            JOIN Car_Class ON Car_Class.Class_Name = Car_Model.Car_Class
            WHERE
                {' AND '.join(conditions)}
            ORDER BY
                Car.VIN ASC
        '''
        )
    ).fetchall()

    cars = [dict(row._mapping) for row in result]
    for row in cars:
        for col in row:
            if row[col] is None:
                row[col] = ''

    return templates.TemplateResponse(
        'admin/car_list.html',
        {
            'request': request,
            'user': user,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'headers': cars[0].keys() if len(cars) > 0 else [],
            'cars': cars,
        },
    )

@router.get('/admin/users')
def users_list(
    request: Request,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    address: Optional[str] = None,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)):

    conditions = [
        '1 = 1',
    ]

    if username and username.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(username) LIKE '%{username.lower()}%'")

    if first_name and first_name.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(split_part(customer_name, ' ', 1)) LIKE '%{first_name.lower()}%'")

    if last_name and last_name.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(split_part(customer_name, ' ', 2)) LIKE '%{last_name.lower()}%'")

    if address and address.lower() not in ('none', 'null', ''):
        conditions.append(f"LOWER(customer_address) LIKE '%{address.lower()}%'")

    users = db.execute(
        text(f'''
            SELECT
                split_part(customer_name, ' ', 1) AS first_name,
                split_part(customer_name, ' ', 2) AS last_name,
                customer_address AS address,
                username,
                is_admin
            FROM Users
            WHERE
                {' AND '.join(conditions)}
            ORDER BY last_name, first_name, address ASC

        '''
        )
    ).fetchall()

    return templates.TemplateResponse(
        'admin/user_list.html',
        {
            'request': request,
            'user': user,
            'users': users,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
        },
    )

@router.get('/admin/info')
def admin_info(
    request: Request,
    user = Depends(get_current_admin_user)
):

    return templates.TemplateResponse(
        '/admin/user_info.html',
        {
            'request': request,
            'user': user,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
        },
    )

@router.post('/admin/delete-reservation')
async def delete_reservation(
    request: Request,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):

    data = await request.json()
    customer_name = data['customer_name'].strip()
    customer_address = data['customer_address'].strip()
    pickup_location_id = data['pickup_location_id'].strip()
    pickup_time = data['pickup_time'].strip() + ':00'

    query = f'''
        DELETE FROM Rental_Agreement
        WHERE
            Customer_Name = '{customer_name}' AND
            Customer_Address = '{customer_address}' AND
            Pickup_Location_ID = '{pickup_location_id}' AND
            Pickup_Date_Time = '{pickup_time}'
    '''
    print(query)

    result = db.execute(text(query))
    db.commit()

    deleted_rows = result.rowcount
    print('Deleted rentals:', deleted_rows)

    query = f'''
        DELETE FROM Reservation
        WHERE
            Customer_Name = '{customer_name}' AND
            Customer_Address = '{customer_address}' AND
            Pickup_Location_ID = '{pickup_location_id}' AND
            Pickup_Date_Time = '{pickup_time}'
    '''
    print(query)

    result = db.execute(text(query))
    db.commit()

    deleted_rows = result.rowcount
    print('Deleted reservations:', deleted_rows)
    if deleted_rows != 1:
        raise ValueError(f'Expected 1 reservation to be deleted')

@router.post('/admin/delete-car')
async def delete_car(
    request: Request,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):

    data = await request.json()
    vin = data['vin'].strip()

    vin_in_use_query = 'SELECT 1 FROM Rental_Agreement WHERE LOWER(VIN) = :vin'
    print(vin_in_use_query)
    vin_in_use = db.execute(text(vin_in_use_query), {'vin': vin}).fetchone()
    if vin_in_use:
        raise HTTPException(status_code=400, detail=f'Cannot delete Car with VIN = {vin} since it is in use by a Rental Agreement')

    delete_query = 'DELETE FROM Car WHERE LOWER(VIN) = :vin'
    print(delete_query)
    delete_result = db.execute(text(delete_query), {'vin': vin})
    db.commit()

    deleted_rows = delete_result.rowcount
    print('Deleted cars:', deleted_rows)

    if deleted_rows != 1:
        raise ValueError(f'Expected 1 car to be deleted')

@router.get('/admin/queries')
def admin_queries_get(
    request: Request,
    user = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    queryid: Optional[str] = None,
):
    results = {}
    if queryid and queryid not in ('none', 'null', ''):
       query  = QUERIES[queryid]["sql"]
       print(query)
       results = db.execute(text(query)).fetchall()
       results = [dict(r._mapping) for r in results]
       for row in results:
            for col in row:
                if row[col] is None:
                    row[col] = ''


    return templates.TemplateResponse(
        'admin/queries.html',
        {
            'request': request,
            'user': user,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
             'results': results,
        },
    )
