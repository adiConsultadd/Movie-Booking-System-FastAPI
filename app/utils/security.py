from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError
from app.models.user import User
from typing import Annotated
from passlib.context import CryptContext
from app.config import SECRET_KEY, ALGORITHM

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_hash(currentPassword):
    hashed_password=bcrypt_context.hash(currentPassword)
    return hashed_password

def verify_hash(currentPassword, hashedPassword):
    if not bcrypt_context.verify(currentPassword, hashedPassword):
        return False
    else:
        return True

def authenticate_user(username:str, password:str, db):
    print(SECRET_KEY, " ", ALGORITHM)
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if (verify_hash(password,user.hashed_password)==False):
        return False
    return user

def create_access_token(username:str, user_id, is_admin, expires_delta:timedelta):
    encode = {'sub' : username, 'id':user_id, "is_admin": is_admin}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires}) 
    print(f"Using ALGORITHM: {ALGORITHM}")
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username  = payload.get('sub')
        user_id = payload.get('id') 
        is_admin = payload.get("is_admin")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        
        return {'username': username,  'id': user_id, "is_admin": is_admin}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')