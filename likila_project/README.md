# Likila Travel & Tours — Django Backend

## Stack
- Python 3.12 + Django 6
- Django REST Framework + SimpleJWT
- SQLite database (zero setup)
- django-cors-headers (for the frontend)

## Quick Start

```bash
# 1. Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers pillow

# 2. Run migrations
python manage.py migrate

# 3. Seed demo data + create admin user
python manage.py seed

# 4. Start the server
python manage.py runserver
# → http://127.0.0.1:8000
``


### Dashboard
| Method | URL | Auth |
|--------|-----|------|
| GET | `/api/dashboard/` | ✅ |

### Events
| Method | URL | Auth | Notes |
|--------|-----|------|-------|
| GET | `/api/events/` | No | Public sees upcoming/active only |
| GET | `/api/events/?status=draft` | ✅ | Admin sees all |
| GET | `/api/events/?search=afriski` | No | Search by name |
| POST | `/api/events/` | ✅ | Create (multipart for image upload) |
| PUT | `/api/events/<id>/` | ✅ | Full update |
| PATCH | `/api/events/<id>/` | ✅ | Partial update |
| PATCH | `/api/events/<id>/set_status/` | ✅ | Quick status change |
| DELETE | `/api/events/<id>/` | ✅ | Delete |

### Services
| Method | URL | Auth |
|--------|-----|------|
| GET | `/api/services/` | No |
| POST | `/api/services/` | ✅ |
| PUT/PATCH | `/api/services/<id>/` | ✅ |
| PUT | `/api/services/reorder/` | ✅ |
| DELETE | `/api/services/<id>/` | ✅ |

### Gallery
| Method | URL | Auth |
|--------|-----|------|
| GET | `/api/gallery/` | No |
| GET | `/api/gallery/?limit=5` | No |
| POST | `/api/gallery/` | ✅ |
| PUT/PATCH | `/api/gallery/<id>/` | ✅ |
| PUT | `/api/gallery/reorder/` | ✅ |
| DELETE | `/api/gallery/<id>/` | ✅ |

### Inquiries
| Method | URL | Auth |
|--------|-----|------|
| POST | `/api/inquiries/` | No (public contact form) |
| GET | `/api/inquiries/` | ✅ |
| GET | `/api/inquiries/?is_read=0` | ✅ |
| GET | `/api/inquiries/<id>/` | ✅ (auto-marks read) |
| PATCH | `/api/inquiries/<id>/mark_read/` | ✅ |
| PATCH | `/api/inquiries/mark_all_read/` | ✅ |
| DELETE | `/api/inquiries/<id>/` | ✅ |

### Settings
| Method | URL | Auth |
|--------|-----|------|
| GET | `/api/settings/public/` | No |
| GET | `/api/settings/` | ✅ |
| PUT | `/api/settings/` | ✅ |

---

## Connecting the Frontend



## Django Admin (built-in)
Full CRUD 
available at: `http://127.0.0.1:8000/django-admin/`
Login with the same admin credentials.

---

## Project Structure
```
likila_project/
├── manage.py
├── db.sqlite3              ← Created after migrate
├── media/                  ← Uploaded photos stored here
│   ├── events/
│   ├── gallery/
│   └── services/
├── likila_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/
    ├── models.py           ← Event, Service, GalleryPhoto, Inquiry, SiteSetting
    ├── serializers.py
    ├── views.py            ← All API views
    ├── urls.py             ← All API routes
    ├── permissions.py      ← IsAdminOrReadOnly, IsAdminUser
    ├── admin.py            ← Django admin config
    └── management/commands/
        └── seed.py         ← python manage.py seed
```

## Re-seed at any time
```bash
python manage.py seed --flush   # Clear everything and re-seed
python manage.py seed           # Add missing seed data only
```
