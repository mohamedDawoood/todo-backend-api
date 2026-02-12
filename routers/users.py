from fastapi import APIRouter, Depends, HTTPException , Request
from datetime import timedelta
from starlette import status
from starlette.responses import HTMLResponse

from models import User
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from routers.auth import UserRequest, db_dependency, crypt_context, Token, authenticate_user, \
    create_access_token, user_dependency
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/users", tags=["Users"])



templates = Jinja2Templates(directory="templates")

### pages ###

@router.get("/login-page" )
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register-page")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def signup(create_user_request: UserRequest, db: db_dependency):


    existing_username = db.query(User).filter(User.username == create_user_request.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username is already taken. Try another one.")

    existing_email = db.query(User).filter(User.email == create_user_request.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email is already registered.")

    existing_phone = db.query(User).filter(User.phone_number == create_user_request.phone_number).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number is already registered.")


    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role="user",
        hashed_password=crypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}

from starlette.responses import JSONResponse


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))


    response = JSONResponse(content={
        "access_token": token,
        "token_type": "bearer",
        "user_role": user.role
    })
    response.set_cookie(key="access_token", value=token, httponly=True)

    return response


@router.put("/update" )
async def update(request: UserRequest, db: db_dependency , current_user: user_dependency):
    user = db.query(User).filter(User.id == current_user.get('id')).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                            )
    if user.id != current_user.get('id'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not allowed")
    user.first_name = request.first_name
    user.last_name = request.last_name
    user.phone_number = request.phone_number
    user.email = request.email
    user.hashed_password = crypt_context.hash(request.password)

    db.commit()
    db.refresh(user)
    return user


