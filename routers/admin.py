from typing import Annotated

from fastapi import HTTPException, Path, Depends, APIRouter

from starlette import status
from models import Todo, User
from routers.auth import db_dependency, is_admin

admin_dependency = Annotated[User , Depends(is_admin) ]


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_by_admin(db: db_dependency, current_user: admin_dependency):

    return db.query(Todo).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_admin(db: db_dependency, current_user: admin_dependency, todo_id: int = Path(gt=0)):

    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()


