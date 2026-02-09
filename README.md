<img width="1470" height="801" alt="image" src="https://github.com/user-attachments/assets/fe6be085-c1a9-4031-9abb-57b4cc9ec89d" />

# Learnify AI 🚀  
A full-stack **e-learning platform** with **role-based course management**, **Stripe subscriptions**, and an **AI Tutor** (premium-only).

> Built for learning + portfolio purposes (SaaS-style subscription + AI features).

---

## ✨ Features

### 🔐 Authentication & Roles
- JWT-based login/register
- Roles: **student**, **instructor**, **admin**
- Role-based access control (RBAC)

### 📚 Courses & Lessons
- Instructors/Admin can:
  - Create courses & lessons
  - Publish / unpublish courses
- Students can:
  - View **published** courses only
  - Enroll in courses
  - Track lesson progress

### 💳 Stripe Subscriptions (Premium)
- Users can upgrade using **Stripe Checkout**
- Stripe **webhooks** update user premium status
- Premium users unlock AI features

### 🤖 AI Tutor (Premium only)
- Ask questions through AI endpoint/UI
- Restricted for non-premium users

---

## 🧱 Tech Stack

**Backend**
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- Stripe SDK + Webhooks
- Groq API (AI)

**Frontend**
- SvelteKit (Vite)

---

## 📁 Project Structure (Simplified)
Learnify-AI/
backend/
app/
api/routes/
core/
db/
models/
schemas/
alembic/
.env
frontend/
src/routes/
.env

---

## ✅ Prerequisites
- Python 3.10+ (you are using 3.14 ✅)
- Node.js 18+ (recommended)
- PostgreSQL (local or Docker)
- Stripe account (Sandbox/Test mode)
- Groq API key

---

# ⚙️ Setup Guide

## 1) Clone & Install

```bash
git clone <YOUR_REPO_URL>
cd Learnify-AI
2) Run Database (Docker)

Run this inside the backend/ folder.

cd backend
docker compose up -d


Postgres will run on:

Host: localhost

Port: 5433

DB: learnify

User: postgres

Pass: postgres

3) Backend Setup
Create venv + install

Inside backend/:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create .env in backend/
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/learnify
JWT_SECRET=super-secret-local
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID=price_...

FRONTEND_URL=http://localhost:5173

# Groq
GROQ_API_KEY=gsk_...
GROQ_MODEL=<YOUR_GROQ_MODEL_NAME>


✅ Notes:

STRIPE_SECRET_KEY = starts with sk_test_

STRIPE_PRICE_ID = from Stripe product pricing

STRIPE_WEBHOOK_SECRET = from stripe listen

4) Run Alembic Migrations

Inside backend/:

alembic upgrade head

5) Start Backend API

Inside backend/:

uvicorn app.main:app --reload --port 8000


Backend runs at:
➡️ http://127.0.0.1:8000

6) Stripe Webhook Listener (Local)

Open a new terminal:

stripe listen --forward-to localhost:8000/webhooks/stripe


Copy the shown webhook secret and set:

STRIPE_WEBHOOK_SECRET=whsec_...

7) Frontend Setup

Inside frontend/:

cd ../frontend
npm install
npm run dev


Frontend runs at:
➡️ http://localhost:5173

Create .env in frontend/
PUBLIC_API_URL=http://127.0.0.1:8000



🧪 Testing
✅ Auth

Register user

Login

Check profile /me



✅ Courses

Instructor/Admin: create course → publish

Student: can view only published courses



✅ Stripe Upgrade Flow

Click Upgrade

Complete Stripe test checkout

Webhook should mark is_premium=true

AI Tutor becomes available



✅ Stripe Test Card:

Card: 4242 4242 4242 4242

Exp: any future date

CVC: any 3 digits



🔌 API Endpoints (Main)
Auth

POST /auth/register

POST /auth/login

User

GET /users/me

Courses

GET /courses

POST /courses (instructor/admin)

POST /courses/{id}/publish (instructor/admin)

Billing

POST /billing/create-checkout-session

Webhook

POST /webhooks/stripe

AI Tutor

POST /ai/ask (premium only)



🚀 Future Improvements

Better UI (dashboard layout + badges)

Admin panel for managing users

Subscription status page

Lesson quizzes + certificates

CI/CD pipeline (GitHub Actions + Docker)
