# Jira-like Ticketing System with Flask & MySQL

A simplified ticketing system inspired by Jira, built with Flask (Python), MySQL, and HTML/CSS. Includes user authentication, role-based access control, and ticket management.


## Features

- **User Authentication**
  - Registration & login/logout
  - Password hashing with Flask-Bcrypt
- **Ticket Management**
  - Create/view tickets
  - User-specific ticket ownership
- **Role-Based Access Control**
  - Admin/user roles
  - Admin dashboard for all tickets
- **Database**
  - MySQL relational database
  - SQLAlchemy ORM integration

## Technologies

- **Backend**: Python 3, Flask
- **Database**: MySQL, Flask-SQLAlchemy
- **Authentication**: Flask-Login, Flask-Principal
- **Frontend**: HTML5, CSS3, Jinja2 templating

## Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/bhuvnesha/flask-ticketing-system.git
   cd flask-ticketing-system
Set Up Virtual Environment

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
Install Dependencies

bash
pip install -r requirements.txt
Database Setup

bash
mysql -u root -p
CREATE DATABASE ticketing_db;
QUIT;
Environment Variables
Create .env file:

env
SECRET_KEY=your-random-secret-key
SQLALCHEMY_DATABASE_URI=mysql://username:password@localhost/ticketing_db
Initialize Database

bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
Usage
Start Application

bash
flask run
Create Admin User (First Time)

bash
flask shell
>>> from app import bcrypt, User
>>> hashed_pw = bcrypt.generate_password_hash('adminpass').decode('utf-8')
>>> admin = User(username='admin', password=hashed_pw, role='admin')
>>> db.session.add(admin)
>>> db.session.commit()
Access in Browser

Regular user: http://localhost:5000

Admin dashboard: http://localhost:5000/admin

Project Structure
├── app.py                 # Main application
├── forms.py               # WTForms definitions
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── static/                # CSS/JS assets
│   └── styles.css
├── templates/             # Jinja2 templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── admin_dashboard.html
└── venv/                  # Virtual environment
Testing
Sample Workflow:

Register new user at /register

Login at /login

Create tickets via dashboard

Admin login: /login (admin/adminpass)

View all tickets at /admin

Test Cases:

python
# Create test users
user1 = User(username='test1', password=hashed_pw)
user2 = User(username='test2', password=hashed_pw)

# Create tickets
Ticket(title='Bug 1', user_id=user1.id)
Ticket(title='Feature 2', user_id=user2.id)
Troubleshooting
Common Issues:

Database Connection Failed: Verify MySQL credentials in .env

CSRF Token Errors: Ensure {{ form.hidden_tag() }} in forms

Admin Access Denied: Confirm user has role='admin' in database

Reset Database:

bash
flask shell
>>> db.drop_all()
>>> db.create_all()
License
MIT License. See LICENSE for details.

Acknowledgments

Flask Documentation

Flask-Login & Flask-Principal teams

MySQL Community Edition
