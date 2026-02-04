from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from database import  SessionLocal
from models import Todo
from typing import Annotated
from .auth import get_current_user

router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# -------------------------------
#            READ ALL
# -------------------------------
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency ,
                   current_user: user_dependency):

    return db.query(Todo).filter(Todo.owner_id == current_user.get("id")).all()


# -------------------------------
#            READ ONE
# -------------------------------
@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency,
                    current_user: user_dependency,
                    todo_id: int = Path(gt=0)):

    read_one_todo = db.query(Todo).filter(Todo.id == todo_id)\
    .filter(Todo.owner_id == current_user.get("id")).first()
    if not read_one_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="NOT FOUND"
                            )
    return read_one_todo



# -------------------------------
#            CREATE
# -------------------------------
@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoRequest, db: db_dependency , current_user : user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")

    todo_model = Todo(**todo.model_dump() , owner_id = current_user.get('id'))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


# -------------------------------
#            UPDATE
# -------------------------------

@router.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    db: db_dependency ,
    current_user: user_dependency ,
    todo_id: int = Path(gt=0),
    todo_request: TodoRequest = None,

                    ):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found")

    if todo_model.owner_id != current_user.get('id'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    for key, value in todo_request.model_dump().items():
        setattr(todo_model, key, value)

    db.commit()
    return {"message" : "this todo has been updated"}


# -------------------------------
#            DELETE
# -------------------------------


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        db: db_dependency ,
        current_user: user_dependency ,
        todo_id: int = Path(gt=0)

                    ):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Todo Not Found")

    if todo_model.owner_id != current_user.get('id'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "You are not authorized to perform this action")


    db.delete(todo_model)
    db.commit()



