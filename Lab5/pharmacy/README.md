# Pharmacy Management System

A Django-based web application for managing a pharmacy, including inventory, sales, and customer interactions.

## Features

- Medicine catalog with categories and search functionality
- User authentication and authorization
- Shopping cart and order management
- News and updates section
- Employee and supplier management
- Reviews and ratings system
- Promotional offers and discounts
- Company information and contact details

## Requirements

- Python 3.8+
- Django 5.2.1
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pharmacy
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Project Structure

- `main/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions
  - `urls.py` - URL configurations
  - `admin.py` - Admin interface configurations
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript, images)
- `media/` - User-uploaded files

## User Types

1. Superuser (Admin)
   - Full access to admin panel
   - Can manage all aspects of the system
   - View sales statistics and reports

2. Authenticated Users
   - Browse and purchase medicines
   - View order history
   - Submit reviews
   - Access personal profile

3. Anonymous Users
   - Browse medicine catalog
   - View basic information
   - Register/Login

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 