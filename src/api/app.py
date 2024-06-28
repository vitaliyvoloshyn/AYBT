from fastapi import FastAPI, APIRouter
from starlette.staticfiles import StaticFiles

from src.api.views import router
from src.html_views.views import html_router

app = FastAPI()
api_router = APIRouter(prefix='/api')
api_router.include_router(router)
app.include_router(api_router)
app.include_router(html_router)

app.mount("/static/css", StaticFiles(directory="static/css"), name='css')
app.mount("/static/js", StaticFiles(directory="static/js"), name='js')
