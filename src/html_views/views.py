from datetime import date

from fastapi import APIRouter, Form
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from schemas.schemas import WorkDayAddDTO
from services import IService

html_router = APIRouter(tags=['HTML'])
template = Jinja2Templates(directory='templates')
service = IService()


@html_router.get('/')
def main_page(request: Request):
    workdays = service.get_fact_wd_per_month(date.today().month, date.today().year)
    return template.TemplateResponse(name='index.html',
                                     context={
                                         'request': request,
                                         'wd': workdays,
                                     })


@html_router.get('/add_wd')
def add_wd_form(request: Request):
    return template.TemplateResponse(request,
                                     name='add_wd.html')


@html_router.post('/add_wd')
def add_wd(wd_date: date = Form(), wd_desc: str = Form()):
    dto = WorkDayAddDTO(date=wd_date, description=wd_desc, day_of_week='')
    try:
        service.add_wd(dto)
    except IntegrityError as e:
        return {'detail': e}

    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)


@html_router.get('/wd')
def get_month_wd(request: Request, month: int, year: int):
    workdays = service.get_fact_wd_per_month(month, year)
    return template.TemplateResponse(name='view_wd.html',
                                     context={
                                         'request': request,
                                         'months': service.month_for_view_wd(month, year),
                                         'wd': workdays,
                                     }
                                     )
