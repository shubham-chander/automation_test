CREATE TABLE IF NOT EXISTS flights (
    id VARCHAR(8) NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL,
    departure_airport VARCHAR(3) NOT NULL,
    arrival_airport VARCHAR(3) NOT NULL,
    departure_timezone VARCHAR(30) NOT NULL,
    arrival_timezone VARCHAR(30) NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    passport_id VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE UNIQUE INDEX IF EXISTS customers__passport_id_idx ON customers (passport_id);


CREATE TABLE IF NOT EXISTS passengers (
    flight_id VARCHAR(8) NOT NULL REFERENCES flights(id),
    customer_id INT NOT NULL REFERENCES customers(id),
    PRIMARY KEY (flight_id, customer_id)
);


INSERT INTO flights VALUES('AAA01', '2024-12-01T00:00:00Z', '2024-12-01T02:00:00Z', 'DMK', 'HYD', 'Asia/Bangkok', 'Asia/Bangkok');
INSERT INTO flights VALUES('AAA02', '2024-12-01T10:00:00Z', '2024-12-01T14:00:00Z', 'LHR', 'BKK', 'Europe/London', 'Asia/Bangkok');
INSERT INTO flights VALUES('AAA03', '2024-12-01T00:00:00Z', '2024-12-01T02:00:00Z', 'DMK', 'CNX', 'Asia/Bangkok', 'Asia/Bangkok');

--INSERT INTO customers (id, passport_id, first_name, last_name) VALUES (1, 'BC1500', 'Shauna', 'Davila');
--INSERT INTO customers (id, passport_id, first_name, last_name) VALUES (2, 'BC1501', 'Shubham', 'Chander');
INSERT INTO customers (id, passport_id, first_name, last_name) VALUES (1, 'BC1502', 'Rock', 'Rose'); -- USED FOR UPDATE TEST CASE
INSERT INTO customers (id, passport_id, first_name, last_name) VALUES (2, 'DELETE', 'John', 'Doe');

-- customers data is keep getting out of sync
SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers));

--INSERT INTO passengers (flight_id, customer_id) VALUES ('AAA01', 1);
INSERT INTO passengers (flight_id, customer_id) VALUES ('AAA01', 1); -- USED FOR UPDATE TEST CASE
INSERT INTO passengers (flight_id, customer_id) VALUES ('AAA01', 2);