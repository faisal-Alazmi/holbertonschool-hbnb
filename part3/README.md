# Part 3

REST API with JWT authentication and role-based access control (admin and regular users).

## Setup

On Windows, use the same Python for pip and run (avoids `ModuleNotFoundError`):

```bash
cd part3
py -3.12 -m pip install -r requirements.txt
py -3.12 run.py
```

Or:

```bash
python -m pip install -r requirements.txt
python run.py
```

## Run

```bash
python run.py
```

Server runs at `http://127.0.0.1:5000`.

- API docs (Swagger): `http://127.0.0.1:5000/api/v1/`
- Health: `http://127.0.0.1:5000/api/v1/health`

## Default admin

A default admin user is created when no users exist:

- Email: `admin@example.com`
- Password: `admin123`

Use it to get a JWT via `POST /api/v1/auth/login`, then call protected endpoints with `Authorization: Bearer <token>`.

## API overview

- **Auth:** `POST /api/v1/auth/login` — returns JWT.
- **Users:** CRUD; create and list require admin; get/update by id allow self or admin.
- **Amenities:** Create and update require admin; list and get are public.
- **Places:** Create/update/delete require auth; only owner or admin can update/delete.
- **Reviews:** Create/update/delete require auth; only review author or admin can update/delete.
