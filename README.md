# Hair Cut Saloon Booking System

A lightweight booking system for a hair saloon with a clean web UI and SQL-backed storage.

## Features
- Browse available services with duration and price.
- Create customer bookings from a form.
- View upcoming bookings on the home page.
- Admin page to list and delete bookings.
- SQLite database schema with starter service data.

## Tech Stack
- **Backend:** Python + Flask
- **Database:** SQLite (SQL schema included)
- **Frontend:** Jinja2 templates + custom CSS

## Project Structure
- `app.py` - Flask app, routes, and database access logic.
- `schema.sql` - SQL schema and default services.
- `templates/` - UI pages.
- `static/style.css` - styling.

## Quick Start
1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open: `http://127.0.0.1:5000`

On first run, `salon.db` is automatically created and initialized from `schema.sql`.

## Main Routes
- `/` - Dashboard with services and upcoming bookings.
- `/book` - Appointment booking form.
- `/admin` - Admin view of all bookings.
