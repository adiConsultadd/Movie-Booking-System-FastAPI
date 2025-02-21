from fastapi import HTTPException, status

# LOGIN REQUIRED
UNAUTHORIZED_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Login Required"
)

# ADMIN ONLY
FORBIDDEN_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Only Admin Can Perform This Action"
)

# Invalid Credentials
INVALID_CREDS = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Username Or Password"
)

# Movie Errors
MOVIE_NOT_FOUND_ERROR = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
)

# Booking Errors
BOOKING_NOT_FOUND_ERROR = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found"
)

# Booking Already Exists
BOOKING_ALREADY_EXISTS_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="You have already booked this movie"
)

# Username Already Exists
USERNAME_ALREADY_EXISTS_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
)


# Invalid Movie Create Data
INVALID_MOVIE_DATA = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalide Movie Data"
)
