DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Rental_Agreement;
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Car;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Car_Model;
DROP TABLE IF EXISTS Car_Class;

CREATE TABLE Car_Class (
    Class_Name VARCHAR(100) PRIMARY KEY,
    Daily_Rate DOUBLE PRECISION,
    Weekly_Rate DOUBLE PRECISION
);

CREATE TABLE Car_Model (
    Model_ID SERIAL PRIMARY KEY,
    Car_Class VARCHAR(100) NOT NULL,
	Make VARCHAR(100) NOT NULL,
    Model VARCHAR(100) NOT NULL,
    Year_ INT NOT NULL,
    FOREIGN KEY (Car_Class) REFERENCES Car_Class(Class_Name)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    UNIQUE (Make, Model, Year_)
);

CREATE TABLE Location (
    Location_ID VARCHAR(100) PRIMARY KEY,
    Address VARCHAR(200) NOT NULL,
    UNIQUE (Address)
);

CREATE TABLE Car (
VIN VARCHAR(100) PRIMARY KEY,
    Location_ID VARCHAR(100) NOT NULL,
    Model_ID INT NOT NULL,
    FOREIGN KEY (Location_ID) REFERENCES Location(Location_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Model_ID) REFERENCES Car_Model(Model_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );

CREATE TABLE Customer (
    Customer_Name VARCHAR(100) NOT NULL,
    Customer_Address VARCHAR(200) NOT NULL,
    PRIMARY KEY (Customer_Name, Customer_Address)
);

CREATE TABLE Reservation (
    Class_Name VARCHAR(100) NOT NULL,
    Customer_Name VARCHAR(100) NOT NULL,
    Customer_Address VARCHAR(200) NOT NULL,
    Pickup_Location_ID VARCHAR(100) NOT NULL,
    Status_ VARCHAR(100),
    Pickup_Date_Time TIMESTAMPTZ NOT NULL,
    Return_Date_Time TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (Customer_Name, Customer_Address, Pickup_location_ID, Pickup_Date_Time),
    FOREIGN KEY (Class_Name) REFERENCES Car_Class(Class_Name)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Customer_Name, Customer_Address) REFERENCES Customer(Customer_Name, Customer_Address)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Pickup_Location_ID) REFERENCES Location(Location_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Rental_Agreement (
    Contract_Number VARCHAR(100) PRIMARY KEY,
    Customer_Name VARCHAR(100) NOT NULL,
    Customer_Address VARCHAR(200) NOT NULL,
    Pickup_Location_ID VARCHAR(100) NOT NULL,
    Pickup_Date_Time TIMESTAMPTZ NOT NULL,
	VIN VARCHAR(100) NOT NULL,
    Start_Date_Time TIMESTAMPTZ,
    Start_Odometer_Reading INT,
    End_Date_Time TIMESTAMPTZ,
    End_Odometer_Reading INT,
    License_State CHAR(2) NOT NULL,
    License_Number VARCHAR(50) NOT NULL,
    License_Expiry_Month INT NOT NULL,
    License_Expiry_Year INT NOT NULL,
    Credit_Card_Type VARCHAR(50) NOT NULL,
    Credit_Card_Number CHAR(16) NOT NULL,
    Credit_Card_Expiry_Month INT NOT NULL,
    Credit_Card_Expiry_Year INT,
    Total_Cost DOUBLE PRECISION,
    FOREIGN KEY (Customer_Name, Customer_Address, Pickup_Location_ID, Pickup_Date_Time) REFERENCES Reservation(Customer_Name, Customer_Address, Pickup_Location_ID, Pickup_Date_Time)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (VIN) REFERENCES Car(VIN)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Users (
    Username VARCHAR(100) PRIMARY KEY,
    Password VARCHAR(200) NOT NULL,
    Is_Admin BOOLEAN NOT NULL DEFAULT FALSE,
    Customer_Name VARCHAR(100) NOT NULL,
    Customer_Address VARCHAR(200) NOT NULL,
    FOREIGN KEY (Customer_Name, Customer_Address) REFERENCES Customer(Customer_Name, Customer_Address)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
