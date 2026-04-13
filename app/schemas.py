from sqlmodel import SQLModel


# Represent one ingredient entry inside a recipe.
class RecipeIngredientBase(SQLModel):
    name: str
    quantity: str | None = None
    unit: str | None = None


# Schema for creating a recipe.
class RecipeCreate(SQLModel):
    title: str
    instructions: str
    ingredients: list[RecipeIngredientBase]


# Schema for returning a recipe.
class RecipeRead(SQLModel):
    id: int
    title: str
    instructions: str
    ingredients: list[RecipeIngredientBase]