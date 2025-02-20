# Movie Ticket Booking System - FastAPI

A simple movie ticket booking system built with FastAPI, implementing role-based access control, JWT authentication, and validation with Pydantic.

---

## 🚀 Features

### **Admin Endpoints** (Requires `is_admin=True`)

- `POST /admin/movies` → Add a new movie
- `PUT /admin/movies/{id}` → Update movie details
- `DELETE /admin/movies/{id}` → Remove a movie
- `GET /admin/movies` → View all available movies
- `GET /admin/bookings` → View all ticket bookings

### **User Endpoints**

- `GET /movies` → View available movies & showtimes
- `POST /movies/{id}/book` → Book a ticket
- `DELETE /movies/{id}/cancel` → Cancel a booking
- `GET /movies/history` → View booking history

---

## 🛠 Tech Stack

- **FastAPI** - Web framework
- **SQLite** - Database (via SQLAlchemy)
- **Pydantic** - Data validation
- **JWT Authentication** - Secure routes
- **Pytest** - Unit testing

---

## 🔧 Installation & Setup

### 1⃣ Clone the Repository

```bash
git clone https://github.com/adiConsultadd/Movie-Booking-System-FastAPI.git
```

### 2⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Mac
venv\Scripts\activate  # For Windows
```

### 3⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4⃣ Set Up Environment Variables

Create a `.env` file and add the following details:

```bash
SECRET_KEY="*************"
ALGORITHM="**************"
```

### 5⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

---

## 🔑 Authentication

- Users & Admins must authenticate using JWT tokens.
- Use the `/auth/login` endpoint to get a token, then pass it in the `Authorization` header:
  ```bash
  Authorization: Bearer <your_token_here>
  ```
- Tokens expire in **20 minutes**.

---

## 📚 Project Structure

```
movie-ticket-booking/
│── app/
│   ├── models/
│   │   ├── booking.py
│   │   ├── movie.py
│   │   ├── user.py
│   ├── routes/
│   │   ├── adminRoute.py
│   │   ├── authRoute.py
│   │   ├── userRoute.py
│   ├── schemas/
│   │   ├── authSchema.py
│   │   ├── bookingSchema.py
│   │   ├── movieSchema.py
│   ├── utils/
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── security.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│── test/
|   |── __init__.py
│   ├── conftest.py
│   ├── test_admin.py
│   ├── test_auth.py
│   ├── test_user.py
│── .env
│── .gitignore
|-- Readme.md
```

---

## 🧠 Running Tests (Pytest)

Tests are divided into three files:

- `test_admin.py` → Tests admin-related endpoints
- `test_auth.py` → Tests authentication mechanisms
- `test_user.py` → Tests user-related endpoints

To run all tests:

```bash
pytest
```

To run a specific test file:

```bash
pytest test/test_admin.py
```

---