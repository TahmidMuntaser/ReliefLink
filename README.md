# ReliefLink

A Proper Distribution of Relief for the Needy

---

## 👋 Welcome
This guide helps a new developer get the project running locally after forking the repo. The project is a Django 5 app using SQLite and environment variables loaded from `.env`.

- Backend: Django 5.x (Python 3.10+ recommended)
- DB: SQLite (local dev)
- Static: WhiteNoise + Django collectstatic
- Deployment (optional): Vercel (via `vercel.json`)

Repository layout (top-level):

```
<repo-root>/
├─ README.md
└─ ReliefLink/              # Django project root (manage.py lives here)
	 ├─ manage.py
	 ├─ requirements.txt
	 ├─ .env.example         # Template for environment variables (commit this)
	 ├─ .env                 # Your local secrets (DO NOT COMMIT)
	 ├─ account/ global/ home/ Status/ ReliefLink/
	 └─ ...
```

> Important: All Django commands run inside the inner `ReliefLink/` folder where `manage.py` is located.

---

## 🚀 Quick Start (Windows PowerShell)

```powershell
# 1) Fork the repo on GitHub, then clone YOUR fork and enter the repo root
# Replace YOUR_USERNAME with your GitHub username

git clone https://github.com/YOUR_USERNAME/ReliefLink.git
cd ReliefLink

# 2) Go to the Django project folder (where manage.py lives)
cd ReliefLink

# 3) Create and activate a virtual environment
python -m venv venv
./venv/Scripts/Activate.ps1

# If activation is blocked by execution policy, run once in this shell:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 4) Install dependencies
pip install -r requirements.txt

# 5) Create your .env from the example and fill in values
Copy-Item .env.example .env

# Generate a strong Django secret key and paste into .env (SECRET_KEY=...)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 6) Apply migrations and create a superuser (optional but recommended)
python manage.py migrate
python manage.py createsuperuser

# 7) (Optional) Collect static files for whitenoise
python manage.py collectstatic --noinput

# 8) Run the dev server
python manage.py runserver
```

- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## 🔐 Environment Variables
We use `python-dotenv` to load environment variables from `.env`. Do not commit your `.env`—it contains secrets. Commit `.env.example` and keep it updated.

`ReliefLink/.env.example` includes:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

In `ReliefLink/ReliefLink/settings.py`, `SECRET_KEY` is required and must be provided via `.env` or an environment variable. If `SECRET_KEY` is missing, the app will raise an error on startup.

To generate a secure key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📦 Dependencies
Dependencies are listed in `ReliefLink/requirements.txt`. Key packages:
- Django
- python-dotenv
- whitenoise
- gunicorn (for deployment)
- vercel (adapter used by Vercel’s Python runtime)

Install them with:

```powershell
pip install -r requirements.txt
```

---

## 🗂️ Static Files
Static files from apps are collected to `staticfiles/`.

- Collect: `python manage.py collectstatic`
- If you see warning `(staticfiles.W004) ... STATICFILES_DIRS ... does not exist`, either:
	- Create the folder `ReliefLink/static`, or
	- Remove/comment `STATICFILES_DIRS` if you don’t need a project-level static folder (app-level static is enough).

WhiteNoise is already enabled in middleware to serve static files in dev/prod.

---

## 🧰 Common Issues

- Virtualenv Activation blocked
	```powershell
	Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
	./venv/Scripts/Activate.ps1
	```

- SECRET_KEY error
	- Ensure `.env` exists in `ReliefLink/` and contains `SECRET_KEY=...`.

- pip / python not found
	- Try `py -3 -m venv venv` and `py -3 -m pip install -r requirements.txt`.

- Port already in use
	```powershell
	python manage.py runserver 0.0.0.0:8001
	```

---

## 🌐 Deployment (optional: Vercel)
This repo includes `vercel.json`. For production, set environment variables in Vercel:
- `SECRET_KEY` (generate a new one for prod)
- `DEBUG=False`
- `ALLOWED_HOSTS=your-app.vercel.app`
- Email settings as needed

Run collectstatic during build and ensure migrations run as part of your deploy pipeline if you use a writable DB.

---

## 🤝 Contributing
- Open an issue or PR from your fork
- Keep `.env.example` in sync when you add new env vars
- Don’t commit secrets (`.env` is in `.gitignore`)

---

## 📄 License
See `LICENSE` for details.
