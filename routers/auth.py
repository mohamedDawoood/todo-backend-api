import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime , timedelta , timezone
from jose import jwt , JWTError
from pydantic import BaseModel
from starlette import status
from models import User
from database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")




class UserRequest(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str



class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username : str  , password : str , db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not crypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username : str , user_id : int , role : str , expires_delta : timedelta):

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



async def get_current_user(token : Annotated[str , Depends(oauth2_bearer)]):
    try:
        payload =jwt.decode(token , SECRET_KEY, algorithms=[ALGORITHM])
        username  : str = payload.get("sub")
        user_id : int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")
        return { "username" : username , "id" : user_id , "role" : user_role }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")






user_dependency = Annotated[User ,Depends(get_current_user) ]


async def is_admin(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can access this page")
    return current_user

