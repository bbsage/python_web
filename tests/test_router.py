from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoint import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_say_hello_default():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_say_hello_with_name():
    response = client.get("/hello?name=Denny")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Denny!"}
