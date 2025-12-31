# 🏦 E-Just Banking System (Secure & Scalable)

> **A robust banking application built from scratch using Django, designed with advanced Security, OOP Principles, and JWT Authentication.**

---

## 📖 Project Overview
This project is a Banking System simulation built to demonstrate **secure software architecture**. Instead of relying on Django's default "magic," we implemented core components manually to ensure full control and understanding of the underlying mechanics.

### 🚀 Key Features
* **Custom Authentication System:** Built from scratch (No `django.contrib.auth.urls`).
* **JWT Middleware:** Global security layer protecting all routes automatically.
* **OOP Design:** Heavy use of inheritance, encapsulation, and polymorphism.
* **Secure Environment:** Sensitive data managed via `.env` files.

---

## ⚙️ Installation & Setup Guide

Follow these steps to run the project locally.

### 1. Prerequisite: Create Virtual Environment
We isolate our dependencies to keep the system clean.
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```
### 2. Install Dependencies

We need specific libraries for our manual security implementation.
```
pip install django pyjwt bcrypt python-dotenv mysqlclient
```

### 3. Environment Configuration (.env)

We do not hardcode secrets or database passwords. Create a file named .env in the root folder next to manage.py:
```
# .env file
SECRET_KEY=your-super-secret-django-key-here
DEBUG=True

# Database Config
DB_NAME=banking_db
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306

```


### 4. Database Setup & Migrations

Initialize the database tables (Custom User & Profile).
```
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Server
```
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser

## 📂 Project Structure (Simplified)
```
bankingSystem/
│   bankingSystem/
|       ├── templates/
│         ├── base.html
│         └── dashboard.html
│   ├── __init__.py
│   ├── views.py
│   ├── system.py
│   ├── urls.py
│   └── auth_service.py
├── users/
│   ├── models.py
│   ├── views.py
│   ├── middleware.py
│   ├── signals.py
│   └── auth_service.py
│
│
├── manage.py
└── .env
```


### Phase 1: The "Clean Slate" Approach

We started by creating a standard Django project but decided to **delete** the default authentication apps (django.contrib.auth, admin, sessions) from settings.py.

*   **Why?** To implement a pure, stateless architecture using JWTs instead of Sessions.
    
*   **Result:** A lightweight application acting as a secure router.
    



### Phase 2: The Security Engine (Manual Auth)

We implemented a helper class AuthService to handle cryptography.

1.  **Hashing:** We use **Bcrypt** to salt and hash passwords before saving them.
    
2.  **Tokens:** We use **PyJWT** to generate secure access tokens.
    

### Phase 3: Global Middleware (The Gatekeeper)

Instead of manually adding @login\_required to every view (which is prone to human error), we built a **Global Middleware**.

*   **How it works:** It intercepts **every** request before it reaches the view.
    
*   **Logic:**
    
    1.  Checks if the URL is public (like /login/ or /register/).
        
    2.  If not public, it looks for the access\_token cookie.
        
    3.  It decodes the JWT and attaches the User object to request.user.
        
    4.  If the token is invalid, it redirects to Login immediately.
        



### Phase 4: Automation with Signals (Observer Pattern)

To ensure data consistency, we used Django Signals.

*   **Event:** When a User is created (post\_save).
    
*   **Action:** Automatically create a Profile linked to that user.
    
*   **Benefit:** The View doesn't need to worry about creating two database records manually.
    


### Phase 5: Frontend Architecture

We set up a **Global Template Inheritance** system.

*   **base.html**: Contains the Tailwind CSS setup and the Global Navbar.
    
*   **dashboard.html**: Extends the base and injects content.

## sections 

The project is divided into 4 modular applications, each handling a specific domain:

* users: Handles Registration, Login (JWT), and User Profiles.

* accounts: Manages Bank Accounts (Savings/Checking) and Balances.

* transactions: Handles Deposits, Withdrawals, and Money Transfers.

* loans: Manages Loan applications and approval logic.

    




