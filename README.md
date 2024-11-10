# Sales Bot Dashboard

This project is a web-based dashboard for managing various elements of a sales-oriented platform. Built with Django for the backend and HTML/CSS/JavaScript for the frontend, the dashboard provides functionalities to manage clients, products, orders, categories, and more.

## Features

- **User Management**: Add, edit, and manage users with different roles (e.g., Admin, User).
- **Client Management**: Add, view, and manage clients.
- **Product Management**: Add, edit, and manage products, including categories and pricing.
- **Order Management**: Track and manage customer orders with detailed order information.
- **Messages**: Manage messages sent to clients, including feedback requests and promotions.
- **Transmission**: Send broadcasts to all clients in the platform.
- **Payment**: Manage payment keys (PIX) for client transactions.
- **Authentication**: Secure login with user authentication (using Django's built-in authentication system).

## Technologies

- **Backend**: Django 4.x (Python)
- **Frontend**: HTML, CSS (SCSS), JavaScript
- **Database**: SQLite (by default, configurable)
- **Version Control**: Git, GitHub for source control
- **Environment**: Virtual environment using `venv`

## Getting Started

### Prerequisites

Ensure you have the following installed:
- **Python 3.8+**
- **Django 4.x**
- **Git**

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:EduLongen/sales_bot.git
   ```

2. Navigate into the project directory:

   ```bash
   cd sales_bot
   ```

3. Set up a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create the database:

   ```bash
   CREATE DATABASE sales_bot_db;
   ```

6. Apply migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

### File Structure
- **dashboard/**: Contains all views, URLs, templates, and static files (CSS, JS).*
- **templates/**: Holds the HTML files used by Django.*
- **static/**: Holds the static assets (CSS, JavaScript, images).*

### Important Files
- **settings.py**: Django project settings.*
- **urls.py**: Application URLs and routing.*
- **models.py**: Database models.*
- **views.py**: Backend logic handling requests.*
- **requirements.txt**: Project dependencies.*

### Deployment
- To deploy the project, configure the necessary database settings and environment variables. Use services like Heroku or Vercel to host the Django backend.

### Contributing

1. Fork the project.
2. Create a feature branch (git checkout -b feature/AmazingFeature).
3. Commit your changes (git commit -m 'Add some amazing feature').
4. Push to the branch (git push origin feature/AmazingFeature).
5. Open a Pull Request.