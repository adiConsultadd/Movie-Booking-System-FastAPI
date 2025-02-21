from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Annotated

from app.models.user import User
from app.config import SECRET_KEY, ALGORITHM

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_hash(currentPassword: str) -> str:
    """Generate a hashed password."""
    return bcrypt_context.hash(currentPassword)

def verify_hash(currentPassword: str, hashedPassword: str) -> bool:
    """Verify if the provided password matches the stored hash."""
    return bcrypt_context.verify(currentPassword, hashedPassword)

def authenticate_user(username: str, password: str, db) -> User | bool:
    """Authenticate a user by verifying username and password."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_hash(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, is_admin: bool, expires_delta: timedelta) -> str:
    """Generate a JWT access token with expiration."""
    encode = {'sub': username, 'id': user_id, 'is_admin': is_admin, 'exp': datetime.utcnow() + expires_delta}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> dict:
    """Retrieve the current user from the access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        is_admin = payload.get('is_admin')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'is_admin': is_admin}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
