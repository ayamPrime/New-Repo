# VaseCrib

VaseCrib is a Django student-accommodation platform for browsing and posting verified rooms, apartments, and homes.

## Run locally on Replit

1. Install dependencies with `pip install -r requirements.txt`.
2. Apply database migrations with `python manage.py migrate`.
3. Start the development server with `python manage.py runserver 0.0.0.0:5000`.

The development database is SQLite (`db.sqlite3`). The app uses the existing Django apps and session-backed four-step signup flow.

## User preferences

- Preview and approve changes before any GitHub commit or push.
- Keep the existing Django structure and design language when adding features.