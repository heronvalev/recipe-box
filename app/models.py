from sqlmodel import Field, SQLModel


# Link table between recipes and ingredients
class RecipeIngredient(SQLModel, table=True):
    recipe_id: int = Field(foreign_key="recipe.id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredient.id", primary_key=True)
    quantity: str | None = None
    unit: str | None = None


# Define the recipes table
class Recipe(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    instructions: str


# Define the ingredients table
class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str