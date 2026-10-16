# Project Requirements & Context Specification

## 1. Project Overview
**Project Name:** Worker Attendance and Wage Management System (`project1`)  
**Architecture:** Django 4.2 Web Application (MVT Architecture)  
**Database:** SQLite (`db.sqlite3`)  
**Target Environment:** Python 3.9+ (Windows compatible)

This application is a role-based employee attendance and wage calculation platform designed for managing supervisors and daily-wage workers. It enables administrative oversight, supervisor-level attendance logging, automated weekly wage estimation, and secure authentication flows.

---

## 2. User Roles & Access Control

The system supports three user roles defined in the custom `User` model (`accounts.User`):

| Role | Permissions & Capabilities |
| :--- | :--- |
| **Admin (`ADMIN`)** | - Access Admin Dashboard.<br>- Create and manage Supervisors.<br>- Create Workers directly if needed.<br>- Access Django standard admin interface (`/admin/`). |
| **Supervisor (`SUPERWISER`)** | - Access Supervisor Dashboard.<br>- Auto-assigned a unique 5-digit Supervisor Code.<br>- Create, view profile, edit, and delete Workers under their supervision.<br>- Mark daily attendance for assigned workers (`PRESENT`/`ABSENT`).<br>- Review attendance history and daily counts. |
| **Worker (`WORKER`)** | - Access Worker Dashboard.<br>- Auto-assigned a unique 8-digit Worker ID.<br>- View personal attendance log (current week and historical).<br>- View wage summary based on attendance (daily wage rate: ₹300). |

---

## 3. Functional Requirements

### 3.1 Authentication & Account Management (`authentication` & `accounts`)
- **User Registration:** Allows initial user registration with validation (username uniqueness, email uniqueness, minimum password length >= 4 characters).
- **Authentication & Login:** Credentials-based authentication (`username`, `password`) with dynamic role-based redirection:
  - `ADMIN` $\rightarrow$ `/admin_dashboard/`
  - `SUPERWISER` $\rightarrow$ `/superwiser_dashboard/`
  - `WORKER` $\rightarrow$ `/worker_dashboard/`
- **Password Reset Flow:**
  - Request password reset via registered email.
  - Generates a single-use UUID token via `ResetPasword` model with a 10-minute expiry window.
  - Sends reset link via SMTP (`django.core.mail.backends.smtp.EmailBackend`).
- **Worker Management (CRUD by Supervisor):**
  - Create new workers associated with the logged-in supervisor.
  - View worker profile and worker ID.
  - Edit worker details (first name, last name, email, phone number).
  - Delete worker.

### 3.2 Attendance Tracking (`attendance`)
- **Daily Attendance Marking:**
  - Supervisors can select a date and mark each assigned worker as `PRESENT` or `ABSENT`.
  - Database enforces unique attendance per worker per day (`unique_together = ("worker", "date")`).
- **Attendance Records & Reporting:**
  - Supervisor attendance history view showing aggregated counts (total present, total absent) by date.
  - Worker view showing daily attendance statuses.

### 3.3 Wage & Earnings Calculation (`payments` / Worker Dashboard)
- **Base Rate:** Default daily wage of ₹300 per present day.
- **Weekly Wage Calculation:**
  - Calculates start of week (Monday) and end of week (Saturday).
  - Aggregates total present days in the date range.
  - Computes `weekly_earnings = weekly_present * daily_wage` and total accumulated salary.

---

## 4. Technical & System Requirements

### 4.1 Software Prerequisites
- **Python:** Version 3.9 or higher (Python 3.9 - 3.13 supported)
- **Virtual Environment:** `venv` or `virtualenv`

### 4.2 Python Dependencies (`requirements.txt`)
- `Django>=4.2.0,<5.0.0`
- `django-environ>=0.11.0`
- `asgiref>=3.6.0`
- `sqlparse>=0.5.0`
- `typing_extensions>=4.12.0`
- `tzdata>=2024.1` (Required on Windows for timezone offsets)

### 4.3 Environment Variables (`.env`)
Required in the project parent directory (`../.env`) or local configuration:
- `SECRET_KEY`: Django cryptographic signing key.
- `EMAIL_HOST_USER`: Gmail/SMTP sender address.
- `EMAIL_HOST_PASSWORD`: SMTP app password.

---

## 5. Setup & Execution Guide

1. **Activate Virtual Environment:**
   ```powershell
   .\env\Scripts\activate
   ```
2. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Configure Environment:**
   Create a `.env` file based on `.env.example`.
4. **Run Database Migrations:**
   ```powershell
   python manage.py migrate
   ```
5. **Start Development Server:**
   ```powershell
   python manage.py runserver
   ```

