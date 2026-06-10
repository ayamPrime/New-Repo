# El Vanta

El Vanta is a student accommodation rental platform. Launching at Olabisi Onabanjo University in Ago-Iwoye, El Vanta connects students to verified, affordable housing close to campus. Find your home away from home. Inspired by how the biggest platforms started — one school at a time.

---

## Tech Stack

- **Backend:** Python 3.14, Django 6.0.6
- **Database:** SQLite (development), PostgreSQL (production)
- **Version Control:** Git & GitHub

---

## Project Structure

```
startup/
├── venv/               # Virtual environment (not tracked)
├── manage.py           # Django's command-line tool
├── requirements.txt    # Project dependencies
├── hub/                # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/           # User authentication & profiles
├── listings/           # Property & unit listings
└── ratings/            # Reviews & ratings
```

---

## Local Setup

### Prerequisites
- Python 3.14
- Git

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/victorolusegun/el-vanta.git
cd el-vanta
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Apply migrations**
```bash
python manage.py migrate
```

**5. Run the development server**
```bash
python manage.py runserver
```

**6. Open in browser**
```
http://127.0.0.1:8000/
```

---

## Contributing

This project is currently in private development. Contribution guidelines will be added as the project matures.

---

## License

Proprietary. All rights reserved.