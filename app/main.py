from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI

from sqlmodel import Session, select

from app import models
from app.database import create_db_and_tables, get_session
from app.models import Recipe
from app.schemas import RecipeCreate, RecipeRead


# Create a reusable type alias for the database session dependency
SessionDep = Annotated[Session, Depends(get_session)]

# Run startup setup before the app begins serving requests
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# Create the FastAPI app instance
app = FastAPI(lifespan=lifespan)


# Add a simple test route
@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Recipe Box API"}

# Create a new recipe
@app.post("/recipes", response_model=RecipeRead)
def create_recipe(recipe: RecipeCreate, session: SessionDep) -> Recipe:
    db_recipe = Recipe.model_validate(recipe)
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    return db_recipe