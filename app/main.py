from fastapi import FastAPI
from app.routers import users, items
from app.configs.db import database, User
from app.configs.logger import setup_logger

logger = setup_logger()

app = FastAPI(title="FastAPI, Docker, and Traefik")

logger.info("Registering routers...")
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])
logger.info("Routers registered successfully.")


@app.on_event("startup")
async def startup():
    logger.info("Application startup: checking database connection...")
    if not database.is_connected:
        await database.connect()
        logger.info("Database connected.")
    else:
        logger.info("Database already connected.")

    user, created = await User.objects.get_or_create(email="test@test.com")
    if created:
        logger.info("Dummy user created.")
    else:
        logger.info("Dummy user already exists.")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Application shutdown: checking database connection...")
    if database.is_connected:
        await database.disconnect()
        logger.info("Database disconnected.")
    else:
        logger.info("Database was already disconnected.")
