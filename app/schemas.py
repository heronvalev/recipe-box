from sqlmodel import SQLModel


# Define the fields the client must send when creating a recipe
class RecipeCreate(SQLModel):
    title: str
    ingredients: str
    instructions: str


# Define the fields returned by the API when reading a recipe
class RecipeRead(SQLModel):
    id: int
    title: str
    ingredients: str
    instructions: str