# Quick Book

## Overview
Quick Book is a Django REST Framework API that provides a complete event booking platform. It features user authentication, a referral system, event and vendor management, concurrent booking protection, and a custom staff dashboard for administration.

## Features

### Authentication
- User registration and login
- JWT token-based authentication
- Token blacklisting on logout
- Current user profile endpoint
- Strict login rate limiting

### Referral System
- Automatic referral code generation
- Left/Right binary tree structure (ReferralNode)
- Referral tree traversal and building
- Staff/owner-only access to referral data

### Event Management
- Create, list, update, and delete events (Staff-only for modifications)
- Publicly searchable and filterable event listings
- Integrated seat tracking and availability validation

### Booking System
- Customer booking history (including cancelled bookings)
- Concurrent booking protection using `select_for_update()` database row-locking
- Accurate seat availability validation to prevent overbooking
- Booking cancellation and automatic seat restoration

### Vendor Management
- Add, view, and update vendors
- Vendor search functionality

### Custom Staff Dashboard
- Separate from Django's built-in Admin panel
- Staff-only access for administration
- Dashboard statistics (Customers, Vendors, Events, Bookings)
- Comprehensive view of users and their referral trees

### Pagination, search and filtering
- Standardized cursor/page-based pagination
- Advanced search across endpoints using `SearchFilter`
- Field-specific filtering for Events

### API documentation
- Fully auto-generated OpenAPI 3.0 schema
- Swagger UI and ReDoc integration

### Rate limiting
- Global Anonymous and User rate limits
- Stricter isolated limits for Login and Registration endpoints

## Tech Stack
- **Framework:** Django 6.1, Django REST Framework
- **Database:** SQLite3
- **Authentication:** drf-simplejwt
- **Documentation:** drf-spectacular

## Project Structure
- `apps.accounts`: Handles user authentication, registration, login, and JWT logic.
- `apps.referrals`: Manages the binary referral tree and related logic.
- `apps.events`: Handles event creation, updates, and listings.
- `apps.bookings`: Processes reservations, validates seats with locking, and handles cancellations.
- `apps.vendors`: Manages vendor profiles and information.
- `apps.dashboard`: Aggregates administrative views and delegates business logic to core services.

## Setup and Installation

1. **Clone repository:**
   ```bash
   git clone <repository-url>
   cd Quick_Book
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ```

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## Environment Variables
- `SECRET_KEY`: Django secret key for cryptographic signing.
- `DEBUG`: Boolean flag to enable/disable debug mode.

## API Documentation
Once the server is running, you can access the interactive API documentation at:
- **Swagger UI:** `/api/docs/`
- **ReDoc:** `/api/redoc/`
- **OpenAPI Schema:** `/api/schema/`

## Authentication
This API uses JSON Web Tokens (JWT).
To authenticate, obtain an access token via `/api/auth/login/` and include it in your HTTP headers:
```
Authorization: Bearer <your_access_token>
```

## Rate Limiting
- **Anonymous users:** 100 requests per hour
- **Authenticated users:** 1000 requests per hour
- **Login:** 10 requests per minute
- **Registration:** 3 requests per minute
- **Booking Creation:** 5 requests per minute

## API Overview

### Authentication
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `POST /api/auth/token/refresh/`

### Referrals
- `GET /api/referrals/<user_id>/root/`
- `GET /api/referrals/<user_id>/tree/`
- `GET /api/referrals/<user_id>/stats/`

### Events
- `GET /api/events/` (List public events)
- `GET /api/events/<id>/` (View event details)
- `POST /api/events/create/` (Staff only)
- `PATCH /api/events/<id>/update/` (Staff only)
- `DELETE /api/events/<id>/delete/` (Staff only)

### Bookings
- `GET /api/bookings/` (List my bookings)
- `POST /api/bookings/` (Create booking)
- `POST /api/bookings/<id>/cancel/`

### Vendors
- `GET /api/vendors/` (Staff only)
- `POST /api/vendors/` (Staff only)
- `PUT/PATCH /api/vendors/<id>/update/` (Staff only)

### Dashboard
- `GET /api/dashboard/`
- `GET /api/dashboard/users/`
- `GET /api/dashboard/users/<id>/`
- `GET /api/dashboard/users/<id>/referral-tree/`
- `GET /api/dashboard/vendors/`
- `POST /api/dashboard/vendors/`
- `PUT/PATCH /api/dashboard/vendors/<id>/update/`
- `GET /api/dashboard/events/`
- `POST /api/dashboard/events/`
- `PATCH /api/dashboard/events/<id>/update`

## Key Design Decisions
- **Service Layer Pattern:** Business logic is decoupled from DRF views. Controllers/views only handle parsing requests and formatting responses, delegating complex logic to service classes (e.g. `BookingService`, `EventService`).
- **Concurrent Booking Protection:** Overbooking is prevented using database row-level locking (`select_for_update()`) wrapped within an atomic database transaction in the booking service.
- **Access Control Architecture:** Granular permissions using `IsAuthenticated` for regular actions, `IsAdminUser`/`IsStaffUser` for administrative tasks, and `IsOwnerOrAdmin` to securely sandbox sensitive referral data.
- **Pagination & Filtering:** Built-in standard result set pagination is applied globally, paired with `django-filter` to provide composable URL parameters for filtering records.

## Testing
There are currently no automated unit tests implemented in this project. All verification is performed manually via Swagger UI and Django Checks.
