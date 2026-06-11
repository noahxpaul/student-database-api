from fastapi import FastAPI

from recipe_api.config import APP_NAME, APP_VERSION
from recipe_api.routers.recipes import router as recipes_router
from recipe_api.routers.ingredients import router as ingredients_router

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.include_router(recipes_router)
app.include_router(ingredients_router)


@app.get("/")
def root():
    return {"message": "Recipe Manager API is running"}