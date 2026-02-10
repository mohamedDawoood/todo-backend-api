import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from models import Todo



TEST_URL ="sqlite:///./testdb.db"
engine= create_engine(
    TEST_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal =sessionmaker(  autocommit=False, autoflush=False , bind=engine )

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
def override_det_current_user():
    return {"username": "Dawod" ,
            "role" : "admin" ,
            "id" : 1
    }



client = TestClient(app)

@pytest.fixture
def test_todo():
    todo= Todo(
        owner_id = 1 ,
        title = "learn testing",
        description = "learning testing",
        priority = 1,
        complete = False,
        id = 1
    )

    db =TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()
