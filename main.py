from fastapi import FastAPI ,Request
from database import engine
from models import Base
from routers import todos, admin , users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(engine)


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("login.html" ,{"request":request})



@app.get("/health")
def health():
    return {"status": "ok"}



app.include_router(users.router)
app.include_router(todos.router)
app.include_router(admin.router)


