# Restaurant Homepage

A simple Django-rendered restaurant homepage. The project uses Django views, templates, static CSS, SQLite, and Django Admin to manage restaurant information, restaurant photos, today's recommended dishes, owner-written review highlights, and events.

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

Owner-friendly controls are available at `http://127.0.0.1:8000/owner/` for staff users. Use this page to update homepage details, phone/email contact preference, optional online ordering, restaurant photos, today's and scheduled recommended dishes, owner-written review highlights, discounts, and upcoming events.
