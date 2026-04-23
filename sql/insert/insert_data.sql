INSERT INTO Car_Class (Class_Name, Daily_Rate, Weekly_Rate) VALUES
('Convertible', 45.99, 280),
('Luxury', 59.99, 300),
('Sedan', 30, 200),
('SUV', 40, 250),
('Van', 45, 260),
('Compact', 25, 150),
('Economy', 20, 120),
('Pickup', 50, 300),
('Sports', 70, 400),
('Electric', 55, 330),
('Hybrid', 48, 290),
('Premium SUV', 65, 380),
('Minivan', 42, 240),
('Full-Size', 35, 210),
('Offroad', 60, 350);


INSERT INTO Car_Model (Car_Class, Make, Model, Year_) VALUES
('Convertible', 'Ford', 'Mustang', 2000),
('Sedan', 'Honda', 'Civic', 2015),
('Sedan', 'Toyota', 'Corolla', 2000),
('Van', 'Honda', 'Odyssey', 2022),
('Van', 'Toyota', 'Venza', 2010),
('SUV', 'Honda', 'Accord', 2020),
('Compact', 'Nissan', 'Sentra', 2018),
('Economy', 'Kia', 'Rio', 2019),
('Pickup', 'Ford', 'F-150', 2021),
('Sports', 'Chevrolet', 'Corvette', 2022),
('Electric', 'Tesla', 'Model 3', 2023),
('Hybrid', 'Toyota', 'Prius', 2021),
('Premium SUV', 'BMW', 'X5', 2020),
('Full-Size', 'Chevrolet', 'Impala', 2016),
('Offroad', 'Jeep', 'Wrangler', 2022);


INSERT INTO Location (Location_ID, Address) VALUES
('Dover 1', '1000 5th Street, Dover, DE 02320'),
('Boston Fast Rental', '313 West Street, Boston, MA 03330'),
('New York 1', '100 1st Avenue, New York, NY 01210'),
('New York 2', '200 2nd Avenue, New York, NY 01210'),
('San Francisco Main', '3 Main Street, San Francisco, CA 07770'),
('Chicago Central', '10 Lake Shore Dr, Chicago, IL 60601'),
('Miami Beach', '22 Ocean Dr, Miami, FL 33139'),
('Dallas Hub', '400 Elm St, Dallas, TX 75001'),
('Seattle North', '55 Pine St, Seattle, WA 98101'),
('Los Angeles West', '88 Sunset Blvd, Los Angeles, CA 90001'),
('Denver Airport', '1 Airport Rd, Denver, CO 80014'),
('Phoenix Downtown', '77 Camelback Rd, Phoenix, AZ 85001'),
('Atlanta Central', '33 Peachtree St, Atlanta, GA 30303'),
('Houston Metro', '12 Bay Area Blvd, Houston, TX 77058'),
('Portland East', '9 Hawthorne Blvd, Portland, OR 97214');


INSERT INTO Car (VIN, Location_ID, Model_ID) VALUES
('01234567890', 'Dover 1', 2),
('01234567891', 'Dover 1', 2),
('01234567892', 'New York 1', 1),
('01234567893', 'New York 2', 4),
('01234567894', 'Boston Fast Rental', 5),
('01234567895', 'Boston Fast Rental', 6),
('01234567896', 'Chicago Central', 7),
('01234567897', 'Miami Beach', 8),
('01234567898', 'Dallas Hub', 9),
('01234567899', 'Seattle North', 10),
('11234567890', 'Los Angeles West', 11),
('11234567891', 'Denver Airport', 12),
('11234567892', 'Phoenix Downtown', 13),
('11234567893', 'Atlanta Central', 14),
('11234567894', 'Houston Metro', 15);


INSERT INTO Customer (Customer_Name, Customer_Address) VALUES
('John Smith', '1 North Street, Albany, NY 01555'),
('John Smith', '2 South Street, Buffalo, NY 01555'),
('Kelly Jones', '3 Main Street, Omaha, NE 04555'),
('Sally Banks', '4 Corner Street, Denver, CO 03433'),
('Val Smith', '5 Johnson Drive, New Brunswick, NJ 08818'),
('Peter Miles', '10 River Rd, Trenton, NJ 08810'),
('Maria Lopez', '22 Palm Ave, Miami, FL 33101'),
('Chen Wu', '88 Market St, San Francisco, CA 94103'),
('Ava Patel', '55 Garden St, Chicago, IL 60610'),
('Liam Brown', '77 Oak St, Seattle, WA 98102'),
('Emma Davis', '12 Pine St, Boston, MA 02110'),
('Noah Wilson', '33 Maple St, Dallas, TX 75002'),
('Olivia Clark', '44 Cedar St, Phoenix, AZ 85002'),
('Ethan Hall', '66 Birch St, Atlanta, GA 30304'),
('Sophia Young', '99 Elm St, Portland, OR 97215');


INSERT INTO Reservation (Class_Name, Customer_Name, Customer_Address, Pickup_Location_ID, Status_, Pickup_Date_Time, Return_Date_Time) VALUES
('Sedan', 'John Smith', '1 North Street, Albany, NY 01555', 'Dover 1', NULL, '2026-01-01 06:00:00', '2026-01-03 08:00:00'),
('Sedan', 'John Smith', '1 North Street, Albany, NY 01555', 'Dover 1', NULL, '2026-02-01 06:00:00', '2026-02-03 08:00:00'),
('SUV', 'John Smith', '2 South Street, Buffalo, NY 01555', 'New York 1', 'pending', '2026-02-01 06:00:00', '2026-02-07 08:00:00'),
('SUV', 'Kelly Jones', '3 Main Street, Omaha, NE 04555', 'New York 1', 'pending', '2026-04-01 06:00:00', '2026-04-10 12:00:00'),
('Van', 'Val Smith', '5 Johnson Drive, New Brunswick, NJ 08818', 'Boston Fast Rental', NULL, '2026-04-10 09:00:00', '2026-04-20 09:00:00'),
('Van', 'Val Smith', '5 Johnson Drive, New Brunswick, NJ 08818', 'Boston Fast Rental', 'cancelled', '2026-05-01 09:00:00', '2026-05-10 18:00:00'),
('Compact', 'Peter Miles', '10 River Rd, Trenton, NJ 08810', 'Chicago Central', NULL, '2026-03-01 08:00:00', '2026-03-05 10:00:00'),
('Economy', 'Maria Lopez', '22 Palm Ave, Miami, FL 33101', 'Miami Beach', NULL, '2026-03-10 09:00:00', '2026-03-12 09:00:00'),
('Pickup', 'Chen Wu', '88 Market St, San Francisco, CA 94103', 'San Francisco Main', 'pending', '2026-06-01 07:00:00', '2026-06-08 07:00:00'),
('Sports', 'Ava Patel', '55 Garden St, Chicago, IL 60610', 'Chicago Central', NULL, '2026-07-01 10:00:00', '2026-07-04 10:00:00'),
('Electric', 'Liam Brown', '77 Oak St, Seattle, WA 98102', 'Seattle North', NULL, '2026-08-01 09:00:00', '2026-08-05 09:00:00'),
('Hybrid', 'Emma Davis', '12 Pine St, Boston, MA 02110', 'Boston Fast Rental', NULL, '2026-09-01 08:00:00', '2026-09-03 08:00:00'),
('Premium SUV', 'Noah Wilson', '33 Maple St, Dallas, TX 75002', 'Dallas Hub', NULL, '2026-10-01 06:00:00', '2026-10-08 06:00:00'),
('Full-Size', 'Olivia Clark', '44 Cedar St, Phoenix, AZ 85002', 'Phoenix Downtown', NULL, '2026-11-01 07:00:00', '2026-11-05 07:00:00'),
('Offroad', 'Sophia Young', '99 Elm St, Portland, OR 97215', 'Portland East', NULL, '2026-12-01 08:00:00', '2026-12-10 08:00:00');


INSERT INTO Rental_Agreement (
Contract_Number, Customer_Name, Customer_Address, Pickup_Location_ID, Pickup_Date_Time, VIN,
Start_Date_Time, Start_Odometer_Reading, End_Date_Time, End_Odometer_Reading,
License_State, License_Number, License_Expiry_Month, License_Expiry_Year,
Credit_Card_Type, Credit_Card_Number, Credit_Card_Expiry_Month, Credit_Card_Expiry_Year, Total_Cost
) VALUES
('A00001','John Smith','1 North Street, Albany, NY 01555','Dover 1','2026-01-01 06:00:00','01234567890',
 '2026-01-01 06:00:00',10000,'2026-01-03 06:00:00',12000,'NY','B1234512345',12,2026,'Visa Credit','1234567891234567',12,2027,1000),

('A00002','John Smith','1 North Street, Albany, NY 01555','Dover 1','2026-02-01 06:00:00','01234567891',
 '2026-02-01 07:00:00',20000,NULL,NULL,'NY','B1234512345',12,2026,'Visa Credit','1234567891234567',12,2027,1000),

('A00003','John Smith','2 South Street, Buffalo, NY 01555','New York 1','2026-02-01 06:00:00','01234567895',
 '2026-02-01 07:00:00',30000,NULL,NULL,'NY','B1234512346',12,2027,'Visa Credit','1234567891234560',12,2028,1200),

('A00004','Kelly Jones','3 Main Street, Omaha, NE 04555','New York 1','2026-04-01 06:00:00','01234567895',
 NULL,NULL,NULL,NULL,'NY','B1234512347',12,2027,'TD Bank Debit','1234567891234561',12,2028,NULL),

('A00005','Val Smith','5 Johnson Drive, New Brunswick, NJ 08818','Boston Fast Rental','2026-04-10 09:00:00','01234567894',
 NULL,NULL,NULL,NULL,'NY','B1234512348',12,2029,'Visa Debit','1234567891234562',6,2026,NULL),

('A00006','Peter Miles','10 River Rd, Trenton, NJ 08810','Chicago Central','2026-03-01 08:00:00','01234567896',
 '2026-03-01 08:00:00',15000,'2026-03-05 10:00:00',16000,'NJ','C1111111111',10,2028,'Visa Credit','4000000000000001',10,2029,350),

('A00007','Maria Lopez','22 Palm Ave, Miami, FL 33101','Miami Beach','2026-03-10 09:00:00','01234567897',
 '2026-03-10 09:00:00',5000,'2026-03-12 09:00:00',5400,'FL','D2222222222',8,2027,'Mastercard','5000000000000002',8,2028,200),

('A00008','Chen Wu','88 Market St, San Francisco, CA 94103','San Francisco Main','2026-06-01 07:00:00','01234567898',
 NULL,NULL,NULL,NULL,'CA','E3333333333',5,2029,'Visa Credit','6000000000000003',5,2030,NULL),

('A00009','Ava Patel','55 Garden St, Chicago, IL 60610','Chicago Central','2026-07-01 10:00:00','01234567899',
 '2026-07-01 10:00:00',8000,'2026-07-04 10:00:00',9000,'IL','F4444444444',4,2028,'Visa Credit','7000000000000004',4,2029,600),

('A00010','Liam Brown','77 Oak St, Seattle, WA 98102','Seattle North','2026-08-01 09:00:00','11234567890',
 '2026-08-01 09:00:00',12000,'2026-08-05 09:00:00',13000,'WA','G5555555555',3,2029,'Visa Credit','8000000000000005',3,2030,500),

('A00011','Emma Davis','12 Pine St, Boston, MA 02110','Boston Fast Rental','2026-09-01 08:00:00','11234567891',
 '2026-09-01 08:00:00',9000,'2026-09-03 08:00:00',9500,'MA','H6666666666',2,2028,'Visa Debit','9000000000000006',2,2029,250),

('A00012','Noah Wilson','33 Maple St, Dallas, TX 75002','Dallas Hub','2026-10-01 06:00:00','11234567892',
 '2026-10-01 06:00:00',30000,'2026-10-08 06:00:00',33000,'TX','I7777777777',1,2030,'Mastercard','1000000000000007',1,2031,900),

('A00013','Olivia Clark','44 Cedar St, Phoenix, AZ 85002','Phoenix Downtown','2026-11-01 07:00:00','11234567893',
 '2026-11-01 07:00:00',7000,'2026-11-05 07:00:00',7600,'AZ','J8888888888',11,2027,'Visa Credit','1100000000000008',11,2028,350),

('A00014','Sophia Young','99 Elm St, Portland, OR 97215','Portland East','2026-12-01 08:00:00','11234567894',
 '2026-12-01 08:00:00',4000,'2026-12-10 08:00:00',5000,'OR','K9999999999',10,2029,'Visa Credit','1200000000000009',10,2030,700);
