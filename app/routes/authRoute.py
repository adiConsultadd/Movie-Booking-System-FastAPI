from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.models.user import User
from app.schemas.authSchema import CreateUserRequest, LoginResponse
from app.utils.security import authenticate_user, create_access_token, create_hash
from app.utils.exceptions import USERNAME_ALREADY_EXISTS_ERROR, INVALID_CREDS

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest, db: Annotated[Session, Depends(get_db)]):
    """Register a new user with a unique username and hashed password."""
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise USERNAME_ALREADY_EXISTS_ERROR
    
    hashed_password = create_hash(request.password)
    user = User(username=request.username, hashed_password=hashed_password, is_admin=request.is_admin)
    db.add(user)
    db.commit()
    return {"message": "User created successfully", "is_admin": user.is_admin}

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Annotated[Session, Depends(get_db)]):
    """Authenticate a user and return an access token if credentials are valid."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise INVALID_CREDS
    
    token = create_access_token(str(user.username), user.id, user.is_admin, timedelta(minutes=20))
    return {"message": "Logged In Successfully", "access_token": token, "token_type": "bearer"}
