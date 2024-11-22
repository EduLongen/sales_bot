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

### Instalação

1. Clone o repositório:
   ```bash
   git clone git@github.com:EduLongen/sales_bot.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd sales_bot
   ```

3. Configure um ambiente virtual e ative-o:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

4. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

5. Crie o banco de dados:

   ```bash
   CREATE DATABASE sales_bot_db;
   ```

6. Aplique as migrações para configurar o banco de dados:

   ```bash
   python manage.py migrate
   ```

7. Configure o arquivo `.env`:

   Crie um arquivo `.env` na raiz do projeto
   ```bash
   cp .env.example .env
   ```

   Edite a variável de ambiente do Telegram:
   ```env
   TELEGRAM_BOT_TOKEN= # Seu Token do Bot do Telegram
   ```

8. Execute o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

9. Acesse a aplicação em http://127.0.0.1:8000/

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

### Team
 - Daniel Hartmann
 - Eduardo Corrêa
 - Gabriel Costa
 - Lucas Dreveck
 - Mayumi Bogoni
 - Paola Silva