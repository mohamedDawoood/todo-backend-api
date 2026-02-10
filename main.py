from fastapi import FastAPI
from database import engine
from models import Base
from routers import todos, admin , users

app = FastAPI()

Base.metadata.create_all(engine)


@app.get("/health")
def health():
    return {"status": "ok"}



app.include_router(users.router)
app.include_router(todos.router)
app.include_router(admin.router)


