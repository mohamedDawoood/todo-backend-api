from fastapi import status
from routers.todos import get_current_user , get_db
from test.utils import *



app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_det_current_user




def test_get_all_todos(test_todo):
    response=client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"owner_id": 1,
         "title": "learn testing",
         "description": "learning testing",
         "priority": 1,
         "complete": False ,
         "id": 1},]

def test_get_todo_by_id(test_todo):
    response=client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() =={
        "owner_id" : 1 ,
        "title" : "learn testing",
        "description" : "learning testing",
        "priority" : 1,
        "complete" : False ,
        "id": 1}


def test_get_todo_not_exist(test_todo):
    response=client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail":"NOT FOUND"}


def test_create_todo(test_todo):
    request_data ={
        "owner_id" : 1 ,
        "title" : "learn fastapi",
        "description" : "learning fastapi",
        "priority" : 2,
        "complete" : False ,
        "id": 2}
    response=client.post("/todos", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id ==2).first()
    assert model.title == "learn fastapi"
    assert model.description == "learning fastapi"
    assert model.priority == 2
    assert model.complete == False
    assert model.id == 2
    assert model.owner_id == 1

def test_update_todo(test_todo):
    request_data ={"owner_id" : 1 ,
        "title" : "learn fastapi",
        "description" : "learning fastapi",
        "priority" : 2,
        "complete" : False ,
        "id": 1}

    response=client.put("/todos/1",json=request_data)
    assert response.status_code == status.HTTP_200_OK
    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id ==1).first()

    assert model.title == "learn fastapi"
    assert model.description == "learning fastapi"


def test_update_todo_not_exist(test_todo):
    request_data = {"owner_id": 1,
                    "title": "learn fastapi",
                    "description": "learning fastapi",
                    "priority": 2,
                    "complete": False,
                    "id": 1}

    response = client.put("/todos/999", json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail":"Todo Not Found"}


def test_delete_todo(test_todo):
    response=client.delete("/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model =db.query(Todo).filter(Todo.id==1).first()
    assert model is None



def test_delete_todo_not_exist(test_todo):
    response=client.delete("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() ==  {"detail":"Todo Not Found"}