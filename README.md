# TransitOps-Smart-Transport-Operations-Platform
Odoo hackathon 2026 Problem Statement : TransitOps Smart Transport Operations Platform
# TransitOps - Transport Operations Platform

TransitOps is a comprehensive web-based Enterprise Resource Planning (ERP) application designed for transport, logistics, and fleet management businesses. Built on Django, it provides an intuitive and responsive dashboard to streamline your daily operations.

## Features

- **Dashboard & Analytics**: Real-time KPIs, metrics, and interactive charts.
- **Fleet Management**: Track vehicles, statuses, and manage your entire fleet portfolio.
- **Driver Management**: Manage driver profiles, licenses, and assignments.
- **Trips & Routing**: Monitor active trips, timelines, dispatching, and routing.
- **Maintenance**: Schedule and track vehicle maintenance and repairs.
- **Fuel & Expenses**: Log fuel consumption and operational expenses for cost tracking.
- **Responsive UI**: A modern, Odoo-inspired interface that perfectly adapts to desktop, tablet, and mobile devices.

## Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, CSS3 (Custom Design System), JavaScript, Bootstrap 5
- **Icons**: Bootstrap Icons
- **Charts**: Chart.js
- **Database**: SQLite (default for development) / PostgreSQL (recommended for production)

## Installation & Setup

1. **Clone the repository** (if using git) or extract the project files.
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment**:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```
6. **Create a superuser (admin account)**:
   ```bash
   python manage.py createsuperuser
   ```
7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
8. **Access the application**: Open your web browser and navigate to `http://127.0.0.1:8000/`.

## License

This project is proprietary and confidential.
