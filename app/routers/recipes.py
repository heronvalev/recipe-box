from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Ingredient, Recipe, RecipeIngredient
from app.schemas import RecipeCreate, RecipeIngredientBase, RecipeRead


router = APIRouter()


# Create a reusable type alias for the database session dependency
SessionDep = Annotated[Session, Depends(get_session)]


# Helper: build a recipe response object with its linked ingredients
def build_recipe_read(recipe: Recipe, session: Session) -> RecipeRead:
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

    return RecipeRead(
        id=recipe.id,
        title=recipe.title,
        instructions=recipe.instructions,
        ingredients=ingredients_response,
    )


# Create a new recipe with its ingredients
@router.post("/recipes", response_model=RecipeRead)
def create_recipe(recipe: RecipeCreate, session: SessionDep) -> RecipeRead:

    db_recipe = Recipe(title=recipe.title, instructions=recipe.instructions)
    session.add(db_recipe)
    session.flush()

    recipe_ingredients_response: list[RecipeIngredientBase] = []

    for item in recipe.ingredients:
        existing_ingredient = session.exec(
            select(Ingredient).where(Ingredient.name == item.name)
        ).first()

        if existing_ingredient is None:
            existing_ingredient = Ingredient(name=item.name)
            session.add(existing_ingredient)
            session.flush()

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


# Get all recipes, optionally filtered by ingredient name
@router.get("/recipes", response_model=list[RecipeRead])
def get_recipes(session: SessionDep, ingredient: str | None = None,) -> list[RecipeRead]:
    
    if ingredient is None:
        recipes = session.exec(select(Recipe)).all()

    else:
        matching_ingredients = session.exec(
            select(Ingredient).where(Ingredient.name.contains(ingredient))
        ).all()

        if not matching_ingredients:
            return []

        ingredient_ids = [item.id for item in matching_ingredients]

        recipe_links = session.exec(
            select(RecipeIngredient).where(
                RecipeIngredient.ingredient_id.in_(ingredient_ids)
            )
        ).all()

        recipe_ids = list({link.recipe_id for link in recipe_links})
        recipes = [session.get(Recipe, recipe_id) for recipe_id in recipe_ids]
        recipes = [recipe for recipe in recipes if recipe is not None]

    return [build_recipe_read(recipe, session) for recipe in recipes]


# Get one recipe by its ID
@router.get("/recipes/{recipe_id}", response_model=RecipeRead)
def get_recipe(recipe_id: int, session: SessionDep) -> RecipeRead:

    recipe = session.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return build_recipe_read(recipe, session)


# Delete one recipe by its ID
@router.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, session: SessionDep) -> None:

    recipe = session.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe_links = session.exec(
        select(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe.id)
    ).all()

    for link in recipe_links:
        session.delete(link)

    session.delete(recipe)
    session.commit()


# Update one recipe by its ID
@router.put("/recipes/{recipe_id}", response_model=RecipeRead)
def update_recipe(recipe_id: int, updated_recipe: RecipeCreate, session: SessionDep) -> RecipeRead:
    
    recipe = session.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipe.title = updated_recipe.title
    recipe.instructions = updated_recipe.instructions

    recipe_links = session.exec(
        select(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe.id)
    ).all()

    for link in recipe_links:
        session.delete(link)

    for item in updated_recipe.ingredients:

        existing_ingredient = session.exec(
            select(Ingredient).where(Ingredient.name == item.name)
        ).first()

        if existing_ingredient is None:
            existing_ingredient = Ingredient(name=item.name)
            session.add(existing_ingredient)
            session.flush()

        recipe_ingredient_link = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=existing_ingredient.id,
            quantity=item.quantity,
            unit=item.unit,
        )

        session.add(recipe_ingredient_link)
    
    session.commit()

    return build_recipe_read(recipe, session)

