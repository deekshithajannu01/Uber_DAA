CREATE DATABASE IF NOT EXISTS ride_hailing_intelligence;
USE ride_hailing_intelligence;

DROP TABLE IF EXISTS fact_bookings;
DROP TABLE IF EXISTS dim_vehicle;
DROP TABLE IF EXISTS dim_location;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_vehicle (
    vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_type VARCHAR(100) UNIQUE
);

CREATE TABLE dim_location (
    location_id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(100),
    location_name VARCHAR(150),
    UNIQUE KEY unique_location (city, location_name)
);

CREATE TABLE dim_date (
    date_key DATE PRIMARY KEY,
    year_num INT,
    month_num INT,
    day_num INT,
    day_name VARCHAR(20),
    is_weekend BOOLEAN
);

CREATE TABLE fact_bookings (
    booking_sk BIGINT PRIMARY KEY AUTO_INCREMENT,
    booking_id VARCHAR(100),
    booking_datetime DATETIME,
    booking_date DATE,
    pickup_location_id INT,
    drop_location_id INT,
    vehicle_id INT,
    booking_status VARCHAR(100),
    is_cancelled BOOLEAN,
    ride_distance DECIMAL(10,2),
    booking_value DECIMAL(12,2),
    driver_rating DECIMAL(4,2),
    customer_rating DECIMAL(4,2),
    payment_method VARCHAR(100),
    wait_time DECIMAL(10,2),
    hour_num INT,
    day_of_week INT,
    is_peak_hour BOOLEAN,
    fare_per_km DECIMAL(10,2),
    customer_cancel_reason VARCHAR(255),
    driver_cancel_reason VARCHAR(255),
    FOREIGN KEY (booking_date) REFERENCES dim_date(date_key),
    FOREIGN KEY (pickup_location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY (drop_location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY (vehicle_id) REFERENCES dim_vehicle(vehicle_id)
);
