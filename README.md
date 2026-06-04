# Restaurant Homepage

A simple Django-rendered restaurant homepage. The project uses Django views, templates, static CSS, SQLite, and Django Admin for content management.

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open the public homepage at `http://127.0.0.1:8000/` and manage content at `http://127.0.0.1:8000/admin/`.
