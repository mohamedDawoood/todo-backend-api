import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Path
from datetime import datetime , timedelta , timezone
from jose import jwt , JWTError
from pydantic import BaseModel
from starlette import status
from models import User, Todo
from database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["auth"])

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
    role: str


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


admin_dependency = Annotated[User , Depends(is_admin) ]




@router.post("/register", status_code=status.HTTP_201_CREATED)
async def signup(create_user_request: UserRequest, db: db_dependency):


    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role="user",
        hashed_password=crypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

    return create_user_model

@router.post("/login", response_model= Token, status_code=status.HTTP_200_OK)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                        db: db_dependency ):

    user = authenticate_user(form_data.username , form_data.password , db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")

    token = create_access_token(user.username , user.id, user.role , timedelta(minutes=20))



    return {"access_token" : token, "token_type" : "bearer"}


# -------------------------------
#            ADMIN ROUTE
# -------------------------------

@router.get("/admin/todo", status_code=status.HTTP_200_OK)
async def read_all_by_admin(db: db_dependency, current_user: admin_dependency):

    return db.query(Todo).all()


@router.delete("/admin/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_admin(db: db_dependency, current_user: admin_dependency, todo_id: int = Path(gt=0)):

    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()
