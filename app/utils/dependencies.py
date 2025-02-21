from fastapi import Depends, HTTPException, status
from app.utils.security import get_current_user
from app.utils.exceptions import FORBIDDEN_ERROR, UNAUTHORIZED_ERROR


def is_admin(user: dict = Depends(get_current_user)):
    """Dependency to check if user is an admin."""
    if not user["is_admin"]:
        raise FORBIDDEN_ERROR
    return user


def is_authenticated(user: dict = Depends(get_current_user)):
    """Dependency to check if user is authenticated."""
    if not user:
        raise UNAUTHORIZED_ERROR
    return user
