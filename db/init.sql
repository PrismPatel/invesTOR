-- db/init.sql

DROP TABLE IF EXISTS properties;

CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    zpid TEXT UNIQUE,
    address TEXT,
    zipcode TEXT,
    price INTEGER,
    bedrooms INTEGER,
    bathrooms INTEGER,
    area INTEGER,
    home_type TEXT,
    status TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    days_on_market INTEGER,
    broker_name TEXT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
