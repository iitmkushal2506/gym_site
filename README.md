# IRONFORGE FITNESS ⚡
### Premium Full-Stack Commercial Gym Web Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

---

## 1. Project Overview

**IRONFORGE FITNESS** is a production-ready, full-stack web application designed for commercial gyms, fitness clubs, and athletic training centers. 

Unlike static portfolio templates, this platform delivers complete business utility:
- **Automated Lead Generation**: Captures free trial passes and personal training consultation requests.
- **Double-Booking Protection**: Prevents scheduling conflicts by validating coach availability in real time.
- **Interactive 9:16 Instagram Reels Showcase**: Engages prospects with mobile-first video content and direct Instagram links.
- **Non-Technical Admin Portal**: Allows gym owners to manage memberships, coaches, timetables, facility zones, transformation stories, and leads without touching code.

---

## 2. Key Features

### 🌟 Public Experience
- **High-Converting Hero & Statistics Bar**: Live stats counter, dynamic trust indicators, and VIP pass CTAs.
- **Database-Driven Membership Plans**: Dynamic pricing cards with feature comparisons and billing cycles.
- **Coach & Trainer Roster**: In-depth coach bios, certifications, specialties, and 1-click consultation scheduling.
- **Weekly Class Timetable**: Day-by-day interactive timetable with start/end times and trainer assignments.
- **Visual Facility Showroom**: High-definition categorized tour of strength, cardio, and recovery zones.
- **Transformation Showcase**: Interactive before/after comparisons with member stories and stats.
- **Interactive 9:16 Instagram Reels Showcase**: Modal video player and direct Instagram profile linking.
- **Floating WhatsApp Widget & Sticky Mobile Bar**: Instant conversion channels for mobile visitors.

### 🛡️ Business & Admin Portal
- **Secure Flask-Login Authentication**: Salted and hashed passwords with Werkzeug, CSRF protection, and session security.
- **KPI Metrics Dashboard**: Real-time tracking of total leads, pending consultations, active trials, and conversion counts.
- **Unified Lead CRM**: Search, filter, and track leads through lifecycle stages (`NEW`, `CONTACTED`, `CONFIRMED`, `COMPLETED`, `CANCELLED`).
- **Internal Note Logs**: Add timestamps and staff notes to any lead record.
- **Full Content CRUD**: Manage Memberships, Trainers, Classes, Facilities, Transformations, Testimonials, and Instagram Reels.

---

## 3. Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python 3.11, Flask 3.x, Flask Blueprints |
| **Database & ORM** | SQLAlchemy 2.0, PostgreSQL (Production) / SQLite (Local Fallback) |
| **Authentication & Security** | Flask-Login, Werkzeug Password Hashing, Flask-WTF (CSRF) |
| **Forms & Validation** | WTForms, email-validator |
| **Email Service** | Flask-Mail, SMTP Support with Safe Console Fallback |
| **Frontend** | HTML5, Modern CSS3 Design System, JavaScript (ES6+), Bootstrap 5.3, Jinja2 |
| **Typography** | Google Fonts (`Outfit` & `Inter`) |
| **WSGI Server** | Gunicorn |
| **Deployment** | GitHub + Render (Blueprint Ready) |

---

## 4. Folder Structure

```
GYM_site/
├── app/
│   ├── __init__.py          # App factory, blueprints, Jinja context processors & error handlers
│   ├── config.py            # Development and Production configuration
│   ├── extensions.py        # SQLAlchemy, LoginManager, CSRFProtect, Mail
│   ├── models.py            # 12 SQLAlchemy models & relationships
│   ├── forms.py             # WTForms for bookings, auth, and CRUD
│   ├── email_service.py     # Email notifications for clients and gym staff
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # Public pages, timetable, transformations, SEO
│   │   ├── booking.py       # Trial & consultation booking with slot validator
│   │   ├── contact.py       # Enquiry submissions & leads
│   │   ├── auth.py          # Admin login & logout
│   │   └── admin.py         # Full admin dashboard & CRUD controllers
│   ├── templates/
│   │   ├── base.html        # Main public base layout with sticky nav & WhatsApp
│   │   ├── home.html        # Hero, stats, features, dynamic sections, reels
│   │   ├── about.html       # Brand story, timeline, stats
│   │   ├── membership.html  # Dynamic pricing cards & FAQ
│   │   ├── trainers.html    # Coach roster & specialty filters
│   │   ├── trainer_detail.html # Coach bio, classes, direct booking
│   │   ├── classes.html     # Weekly timetable grid with day filters
│   │   ├── facilities.html  # Facility visual gallery
│   │   ├── transformations.html # Before/After showcases
│   │   ├── contact.html     # Lead form, map embed, business info
│   │   ├── book_trial.html  # High-conversion free trial landing form
│   │   ├── book_consultation.html # Consultation booking with double-booking checks
│   │   ├── success.html     # Booking receipt & WhatsApp quick action
│   │   ├── 404.html         # Custom 404 page
│   │   ├── 500.html         # Custom 500 page
│   │   └── admin/
│   │       ├── base_admin.html # Admin layout with sidebar
│   │       ├── login.html      # Dark admin login
│   │       ├── dashboard.html  # KPI cards & lead queues
│   │       ├── leads.html      # Lead pipeline with search, filter, notes
│   │       ├── trials.html     # Free trial requests manager
│   │       ├── appointments.html # Consultation appointment management
│   │       ├── memberships.html # Membership CRUD
│   │       ├── trainers.html   # Trainers CRUD
│   │       ├── classes.html    # Classes timetable CRUD
│   │       ├── facilities.html # Facility & Gallery CRUD
│   │       ├── transformations.html # Transformations CRUD
│   │       ├── testimonials.html # Testimonials CRUD
│   │       └── instagram.html  # Instagram / Reels management (9:16)
│   └── static/
│       ├── css/
│       │   ├── style.css       # Core design system (dark athletic luxury)
│       │   └── admin.css       # Clean admin dashboard styling
│       ├── js/
│       │   ├── main.js         # Public scripts, video modal, timetable filter
│       │   └── admin.js        # Admin scripts, modal triggers, status update handlers
│       └── images/
├── seed.py                  # Standalone / CLI script for demo data
├── run.py                   # Entrypoint with custom Flask CLI commands
├── requirements.txt         # Dependencies
├── Procfile                 # Render WSGI start command
├── render.yaml              # Render 1-click cloud Blueprint
├── .env.example             # Example environment variables
└── README.md                # Documentation
```

---

## 5. Local Setup

### Prerequisites
- Python 3.10+ installed
- Git installed
- PostgreSQL (optional for local, SQLite works automatically out of the box)

---

## 6. Virtual Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/ironforge-fitness.git
cd ironforge-fitness

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 7. Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your values:
```ini
FLASK_ENV=development
SECRET_KEY=your-custom-secret-key-here
DATABASE_URL=
# Leave DATABASE_URL empty for zero-config local SQLite, or set to:
# postgresql://postgres:password@localhost:5432/ironforge_db
```

---

## 8. PostgreSQL Setup (Optional Local / Required on Cloud)

If using local PostgreSQL:
```sql
CREATE DATABASE ironforge_db;
CREATE USER ironforge_user WITH ENCRYPTED PASSWORD 'ironforge_pass';
GRANT ALL PRIVILEGES ON DATABASE ironforge_db TO ironforge_user;
```

Update your `.env`:
```ini
DATABASE_URL=postgresql://ironforge_user:ironforge_pass@localhost:5432/ironforge_db
```

---

## 9. Database Initialization

Run the initialization:
```bash
python run.py
```
*Note: The application automatically creates all tables and seeds the demo data on the first start!*

---

## 10. Demo Data Seeding

To re-seed or populate the database anytime:

```bash
python run.py seed-db
# OR
python seed.py
```

This seeds:
- **3 Membership Plans** (Basic, Premium, Elite)
- **5 Elite Trainers** with bios, specialties, and certifications
- **8 Timetable Classes** scheduled across the week
- **6 Facility Zones** with high-resolution imagery
- **6 Testimonials** with star ratings
- **5 Transformation Stories** with before/after stats
- **6 Instagram Reels** with 9:16 preview cards and videos
- **Sample Enquiries, Trials, and Consultations**

---

## 11. Admin Setup & Credentials

### Default Demo Credentials:
- **URL**: `http://127.0.0.1:5000/admin/login`
- **Username**: `admin`
- **Password**: `admin123`

### Creating a New Admin:
```bash
python run.py create-admin --username gymowner --email owner@ironforgefitness.com --password YourSecurePassword123
```

---

## 12. Running Locally

```bash
python run.py
```

Open your browser and navigate to:
- **Public Website**: `http://127.0.0.1:5000/`
- **Free Trial Page**: `http://127.0.0.1:5000/book-trial`
- **Consultation Page**: `http://127.0.0.1:5000/book-consultation`
- **Admin Dashboard**: `http://127.0.0.1:5000/admin/dashboard`

---

## 13. GitHub Deployment

```bash
git init
git add .
git commit -m "Initial release: Ironforge Fitness Full-Stack Platform"
git branch -M main
git remote add origin https://github.com/your-username/ironforge-fitness.git
git push -u origin main
```

---

## 14. Render Deployment

### Option A: 1-Click Render Blueprint (Recommended)
1. Push your repository to GitHub.
2. Log into [Render.com](https://render.com).
3. Click **New +** -> **Blueprint**.
4. Connect your `ironforge-fitness` repository.
5. Render will automatically detect `render.yaml`, provision a free **PostgreSQL Database** and a **Web Service**, configure environment variables, install dependencies, and launch with Gunicorn!

### Option B: Manual Render Setup
1. Create a **New PostgreSQL Database** on Render (e.g. `ironforge-db`). Copy the **Internal Database URL**.
2. Create a **New Web Service** connected to your repo.
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
3. Add Environment Variables:
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = *(click generate)*
   - `DATABASE_URL` = *(paste your Render database URL)*
   - `GYM_NAME` = `IRONFORGE FITNESS`
   - `GYM_PHONE` = `+91 98765 43210`
   - `GYM_EMAIL` = `info@ironforgefitness.com`
   - `GYM_WHATSAPP` = `919876543210`
4. Click **Deploy Web Service**.

---

## 15. Future Improvements

- [ ] Online payment gateway integration (Stripe / Razorpay) for instant membership purchases.
- [ ] Member portal with barcode gym check-in pass.
- [ ] Automated SMS / WhatsApp message dispatch via Twilio / Gupshup.
- [ ] Real-time trainer calendar sync with Google Calendar API.

---

**Engineered with discipline by Ironforge Fitness Technical Team.**
