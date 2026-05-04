from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import recipes


# Run startup setup before the app begins serving requests.
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# Create the FastAPI app instance.
app = FastAPI(lifespan=lifespan)


# Register the recipe routes with the main app.
app.include_router(recipes.router)


# Add a simple test route.
@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Recipe Box API"}
