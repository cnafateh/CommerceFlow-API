# Django Commerce API

An enterprise-style E-commerce REST API built with **Django**, **Django REST Framework**, **PostgreSQL**, **Redis**, **Celery**, **Docker**, **JWT Authentication**, and **Swagger/OpenAPI**.

---

## 🚀 Features

- JWT Authentication (Register / Login / Refresh)
- Product Catalog
- Category & Brand APIs
- Product Search, Filtering, Ordering & Pagination
- Shopping Cart
- Checkout Flow
- Order Management
- Payment Simulation
- Asynchronous Tasks with Celery & Redis
- Django Signals
- PostgreSQL Database
- Dockerized Development Environment
- Swagger / OpenAPI Documentation
- Automated API Testing with Pytest
- GitHub Actions Continuous Integration (CI)

---

## 🛠 Tech Stack

- Python 3.13
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker & Docker Compose
- Pytest
- Simple JWT
- drf-spectacular (Swagger/OpenAPI)

---

## 📦 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/cnafateh/CommerceFlow-API.git
cd django-commerce-api
```

### 2. Create environment file

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### 3. Run the project

```bash
docker compose up --build
```

### 4. Apply migrations

Open another terminal:

```bash
docker compose exec web python manage.py migrate
```

### 5. Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## 📚 API Documentation

Swagger UI:

```text
http://127.0.0.1:8080/api/docs/
```

OpenAPI Schema:

```text
http://127.0.0.1:8080/api/schema/
```

Admin Panel:

```text
http://127.0.0.1:8080/admin/
```

---

## 🧪 Running Tests

Run all tests inside Docker:

```bash
docker compose run --rm web pytest
```

---

## 🔗 Main API Endpoints

### Authentication

| Method | Endpoint |
|--------|----------|
| POST | `/api/auth/register/` |
| POST | `/api/auth/login/` |
| POST | `/api/auth/refresh/` |

### Products

| Method | Endpoint |
|--------|----------|
| GET | `/api/products/` |
| GET | `/api/products/{slug}/` |
| GET | `/api/categories/` |
| GET | `/api/brands/` |

### Cart

| Method | Endpoint |
|--------|----------|
| GET | `/api/cart/` |
| POST | `/api/cart/items/` |
| PATCH | `/api/cart/items/{id}/` |
| DELETE | `/api/cart/items/{id}/delete/` |

### Orders

| Method | Endpoint |
|--------|----------|
| POST | `/api/orders/checkout/` |

### Payments

| Method | Endpoint |
|--------|----------|
| POST | `/api/payments/{order_id}/` |

---

## 🔄 Example User Flow

1. Register or login.
2. Obtain JWT access token.
3. Browse available products.
4. Add products to cart.
5. Checkout the cart.
6. Complete payment.
7. A Celery background task is triggered after successful payment.

---

## ✨ Project Highlights

This project demonstrates:

- Clean Django app architecture
- RESTful API design
- JWT-based authentication
- PostgreSQL integration
- Dockerized development workflow
- Redis + Celery asynchronous task processing
- Django Signals
- Automated API testing with Pytest
- Interactive API documentation with Swagger
- CI pipeline with GitHub Actions

---

## 📄 License

This project is developed for educational and portfolio purposes.
