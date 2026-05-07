import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.main import app


# Create an in-memory SQLite database for tests instead of using the real app database
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


# Provide database sessions that use the test database
def get_test_session():
    with Session(test_engine) as session:
        yield session


# Override the app's normal database dependency so routes use the test database
app.dependency_overrides[get_session] = get_test_session

# Reset database tables before each test so tests do not affect each other.
@pytest.fixture(autouse=True)
def reset_test_database():
    SQLModel.metadata.create_all(test_engine)

    yield

    SQLModel.metadata.drop_all(test_engine)


# Create a test client for calling the FastAPI app without running a server
client = TestClient(app)


def test_create_recipe():
    payload = {
        "title": "Potato soup",
        "instructions": "Boil and blend the potatoes.",
        "ingredients": [
            {
                "name": "potato",
                "quantity": "500",
                "unit": "g",
            }
        ],
    }

    response = client.post("/recipes", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "Potato soup"
    assert data["instructions"] == "Boil and blend the potatoes."
    assert data["ingredients"][0]["name"] == "potato"
    assert data["ingredients"][0]["quantity"] == "500"
    assert data["ingredients"][0]["unit"] == "g"


def test_get_recipe_by_id():
    payload = {
        "title": "Tomato pasta",
        "instructions": "Cook pasta and add tomato sauce.",
        "ingredients": [
            {
                "name": "tomato",
                "quantity": "2",
                "unit": None,
            }
        ],
    }

    create_response = client.post("/recipes", json=payload)
    created_recipe = create_response.json()
    recipe_id = created_recipe["id"]

    response = client.get(f"/recipes/{recipe_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == recipe_id
    assert data["title"] == "Tomato pasta"
    assert data["instructions"] == "Cook pasta and add tomato sauce."
    assert data["ingredients"][0]["name"] == "tomato"


def test_update_recipe():
    original_payload = {
        "title": "Basic soup",
        "instructions": "Boil vegetables.",
        "ingredients": [
            {
                "name": "carrot",
                "quantity": "2",
                "unit": None,
            }
        ],
    }

    create_response = client.post("/recipes", json=original_payload)
    recipe_id = create_response.json()["id"]

    updated_payload = {
        "title": "Updated soup",
        "instructions": "Boil vegetables and blend.",
        "ingredients": [
            {
                "name": "potato",
                "quantity": "3",
                "unit": None,
            }
        ],
    }

    response = client.put(f"/recipes/{recipe_id}", json=updated_payload)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == recipe_id
    assert data["title"] == "Updated soup"
    assert data["instructions"] == "Boil vegetables and blend."
    assert data["ingredients"][0]["name"] == "potato"
    assert data["ingredients"][0]["quantity"] == "3"


def test_delete_recipe():
    payload = {
        "title": "Recipe to delete",
        "instructions": "This recipe will be deleted.",
        "ingredients": [
            {
                "name": "potato",
                "quantity": "1",
                "unit": None,
            }
        ],
    }

    create_response = client.post("/recipes", json=payload)
    recipe_id = create_response.json()["id"]

    delete_response = client.delete(f"/recipes/{recipe_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/recipes/{recipe_id}")

    assert get_response.status_code == 404


def test_get_all_recipes():
    first_payload = {
        "title": "Potato soup",
        "instructions": "Boil potatoes.",
        "ingredients": [
            {
                "name": "potato",
                "quantity": "2",
                "unit": None,
            }
        ],
    }

    second_payload = {
        "title": "Tomato pasta",
        "instructions": "Cook pasta with tomato sauce.",
        "ingredients": [
            {
                "name": "tomato",
                "quantity": "3",
                "unit": None,
            }
        ],
    }

    client.post("/recipes", json=first_payload)
    client.post("/recipes", json=second_payload)

    response = client.get("/recipes")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    recipe_titles = [recipe["title"] for recipe in data]

    assert "Potato soup" in recipe_titles
    assert "Tomato pasta" in recipe_titles


def test_get_recipes_filtered_by_ingredient():
    potato_payload = {
        "title": "Potato soup",
        "instructions": "Boil potatoes.",
        "ingredients": [
            {
                "name": "potato",
                "quantity": "2",
                "unit": None,
            }
        ],
    }

    tomato_payload = {
        "title": "Tomato pasta",
        "instructions": "Cook pasta with tomato sauce.",
        "ingredients": [
            {
                "name": "tomato",
                "quantity": "3",
                "unit": None,
            }
        ],
    }

    client.post("/recipes", json=potato_payload)
    client.post("/recipes", json=tomato_payload)

    response = client.get("/recipes?ingredient=potato")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Potato soup"
    assert data[0]["ingredients"][0]["name"] == "potato"


def test_create_recipe_rejects_blank_title():
    payload = {
        "title": "   ",
        "instructions": "Boil potatoes.",
        "ingredients": [
            {
                "name": "potato",
                "quantity": "2",
                "unit": None,
            }
        ],
    }

    response = client.post("/recipes", json=payload)

    assert response.status_code == 422