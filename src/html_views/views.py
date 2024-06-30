from datetime import date

from fastapi import APIRouter, Form, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from schemas.schemas import WorkDayAddDTO, PaymentAddDTO
from services import IService

html_router = APIRouter(tags=['HTML'])
template = Jinja2Templates(directory='templates')
service = IService()


@html_router.get('/')
def main_page(request: Request):
    month = date.today().month
    year = date.today().year
    workdays = service.get_fact_wd_per_month(month, year)
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
def get_month_wd_fact(request: Request,
                      type: str,
                      month: int = None,
                      year: int = None,
                      ):
    month = date.today().month if not month else month
    year = date.today().year if not year else year
    workdays = []
    try:
        if type == 'fact':
            workdays = service.get_fact_wd_per_month(month, year)
            page = 'view_fact_wd.html'
        elif type == 'plan':
            workdays = service.get_plan_wd_per_month(month, year)
            page = 'view_plan_wd.html'
        else:
            raise Exception("field type must be one of 'fact' or 'plan'")
    except Exception as e:
        return HTTPException(400, detail=str(e))
    return template.TemplateResponse(name=page,
                                     context={
                                         'request': request,
                                         'months': service.month_for_view_wd(month, year),
                                         'wd': workdays,
                                     }
                                     )


@html_router.get('/enter_payment')
def enter_payment_form(request: Request):
    rates = service.get_all_rate()
    return template.TemplateResponse(name='enter_payment_form.html',
                                     context={
                                         'request': request,
                                         'months': service.months,
                                         'rates': rates,
                                     }
                                     )


@html_router.post('/enter_payment')
def add_payment(sum: int = Form(),
                year: int = Form(),
                month: int = Form(),
                rec_date: date = Form(),
                rate: int = Form(),
                ):
    try:
        payment = PaymentAddDTO(
            date=rec_date,
            value=sum,
            billing_date=date(year, month, 1),
            rate_id=rate,
        )
        service.add_pmnt(payment)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    return RedirectResponse('/',  status_code=status.HTTP_303_SEE_OTHER)
