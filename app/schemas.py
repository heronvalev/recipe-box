from pydantic import field_validator
from sqlmodel import SQLModel


# Represent one ingredient entry inside a recipe.
class RecipeIngredientBase(SQLModel):
    name: str
    quantity: str | None = None
    unit: str | None = None

    # Check that ingredient names are not empty or whitespace-only.
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned_value = value.strip().lower()

        if not cleaned_value:
            raise ValueError("Ingredient name cannot be blank")

        return cleaned_value

    # Check that quantity is not empty or whitespace-only if provided.
    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Quantity must be omitted or contain a value")

        return value.strip() if value is not None else None


# Schema for creating a recipe.
class RecipeCreate(SQLModel):
    title: str
    instructions: str
    ingredients: list[RecipeIngredientBase]

    # Check that recipe text fields are not empty or whitespace-only.
    @field_validator("title", "instructions")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        stripped_value = value.strip()

        if not stripped_value:
            raise ValueError("Title/instructions cannot be blank")
        
        return stripped_value
    
    # Check that each recipe includes at least one ingredient.
    @field_validator("ingredients")
    @classmethod
    def validate_ingredients(cls, value: list[RecipeIngredientBase]) -> list[RecipeIngredientBase]:
        if not value:
            raise ValueError("At least one ingredient must be provided")
        
        return value


# Schema for returning a recipe.
class RecipeRead(SQLModel):
    id: int
    title: str
    instructions: str
    ingredients: list[RecipeIngredientBase]