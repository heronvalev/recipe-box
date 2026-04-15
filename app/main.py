from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from app.database import create_db_and_tables, get_session
from app.models import Ingredient, Recipe, RecipeIngredient
from app.schemas import RecipeCreate, RecipeRead, RecipeIngredientBase


# Create a reusable type alias for the database session dependency.
SessionDep = Annotated[Session, Depends(get_session)]


# Run startup setup before the app begins serving requests.
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# Create the FastAPI app instance.
app = FastAPI(lifespan=lifespan)


# Add a simple test route.
@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Recipe Box API"}


# Create a new recipe with its ingredients.
@app.post("/recipes", response_model=RecipeRead)
def create_recipe(recipe: RecipeCreate, session: SessionDep) -> RecipeRead:
    db_recipe = Recipe(title=recipe.title, instructions=recipe.instructions)
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)

    recipe_ingredients_response: list[RecipeIngredientBase] = []

    for item in recipe.ingredients:
        existing_ingredient = session.exec(
            select(Ingredient).where(Ingredient.name == item.name)
        ).first()

        if existing_ingredient is None:
            existing_ingredient = Ingredient(name=item.name)
            session.add(existing_ingredient)
            session.commit()
            session.refresh(existing_ingredient)

        recipe_ingredient_link = RecipeIngredient(
            recipe_id=db_recipe.id,
            ingredient_id=existing_ingredient.id,
            quantity=item.quantity,
            unit=item.unit,
        )
        session.add(recipe_ingredient_link)

        recipe_ingredients_response.append(
            RecipeIngredientBase(
                name=existing_ingredient.name,
                quantity=item.quantity,
                unit=item.unit,
            )
        )

    session.commit()

    return RecipeRead(
        id=db_recipe.id,
        title=db_recipe.title,
        instructions=db_recipe.instructions,
        ingredients=recipe_ingredients_response,
    )


# Get all recipes, optionally filtered by ingredient name.
@app.get("/recipes", response_model=list[RecipeRead])
def get_recipes(
    session: SessionDep,
    ingredient: str | None = None,
) -> list[RecipeRead]:
    if ingredient is None:
        recipes = session.exec(select(Recipe)).all()
    else:
        matching_ingredient = session.exec(
            select(Ingredient).where(Ingredient.name == ingredient)
        ).first()

        if matching_ingredient is None:
            return []

        recipe_links = session.exec(
            select(RecipeIngredient).where(
                RecipeIngredient.ingredient_id == matching_ingredient.id
            )
        ).all()

        recipe_ids = [link.recipe_id for link in recipe_links]
        recipes = [session.get(Recipe, recipe_id) for recipe_id in recipe_ids]
        recipes = [recipe for recipe in recipes if recipe is not None]

    recipe_list: list[RecipeRead] = []

    for recipe in recipes:
        ingredient_links = session.exec(
            select(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe.id)
        ).all()

        ingredients_response: list[RecipeIngredientBase] = []

        for link in ingredient_links:
            db_ingredient = session.get(Ingredient, link.ingredient_id)

            if db_ingredient is not None:
                ingredients_response.append(
                    RecipeIngredientBase(
                        name=db_ingredient.name,
                        quantity=link.quantity,
                        unit=link.unit,
                    )
                )

        recipe_list.append(
            RecipeRead(
                id=recipe.id,
                title=recipe.title,
                instructions=recipe.instructions,
                ingredients=ingredients_response,
            )
        )

    return recipe_list