DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS services;

CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    duration_minutes INTEGER NOT NULL,
    price_usd REAL NOT NULL
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    service_id INTEGER NOT NULL,
    appointment_date TEXT NOT NULL,
    appointment_time TEXT NOT NULL,
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (service_id) REFERENCES services(id)
);

INSERT INTO services (name, duration_minutes, price_usd) VALUES
('Classic Haircut', 30, 20),
('Beard Trim', 20, 12),
('Kids Haircut', 25, 15),
('Haircut + Wash', 45, 28),
('Premium Styling', 60, 40);
