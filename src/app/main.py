from fastapi import FastAPI
from app.core.config import settings
from app.api.api_v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    #await initiate_database()
    print("startup")


@app.on_event("shutdown")
async def shutdown_event():
    print("shutdown")
