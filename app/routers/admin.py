from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
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
