from fastapi import FastAPI
from app.database import engine
from app.models import booking, movie, user
from app.routes import adminRoute, authRoute, userRoute

# Create All The Databases tables
booking.Base.metadata.create_all(bind=engine)
movie.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

# Creating the app
app = FastAPI(
    title="Movie Ticket Booking API 🎬",
    description="An API for booking movie tickets with JWT authentication and role-based access control.",
    version="1.0.0",
)

app.include_router(authRoute.router)  # Auth Routes
app.include_router(adminRoute.router)  # Admin Routes
app.include_router(userRoute.router)  # User Routes
