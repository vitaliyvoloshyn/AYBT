from fastapi import FastAPI
from src.api.views import router

app = FastAPI()
app.include_router(router)
