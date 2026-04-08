from sqlmodel import Field, SQLModel


# Define the recipes table.
class Recipe(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    ingredients: str
    instructions: str