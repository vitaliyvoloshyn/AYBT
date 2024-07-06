from datetime import date
from pprint import pprint

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Form, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from schemas.schemas import WorkDayAddDTO, PaymentAddDTO, PaymentAnalysisDTO, AllPaymentAnalysisDTO, RateValueAddDTO
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
    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)


@html_router.get('/payment_analysis')
def payment_analysis(request: Request):
    all_pa = None
    res = []
    start_date = date(2024, 1, 1)
    cur_date = date(date.today().year, date.today().month, 1) - relativedelta(months=1)
    while start_date <= cur_date:
        wage = service.get_wage_per_month(cur_date.month, cur_date.year)
        payment = service.get_fact_payments_per_month(cur_date.month, cur_date.year, billing=True)
        mn = cur_date.month
        name = service._get_month_name(cur_date.month)
        y = cur_date.year
        try:
            res.append(PaymentAnalysisDTO(
                month_num=mn,
                month_name=name,
                year=y,
                wage=wage.model_dump(),
                payment=payment.model_dump(),
                diff=(payment - wage).model_dump(),
            ))
        except Exception as e:
            print(e)
        cur_date -= relativedelta(months=1)
        all_pa = AllPaymentAnalysisDTO(total_diff=service.total_payment_analysis(res),
                                       total_payment=service.analysis_total_payment(res),
                                       paDTO=res)
    return template.TemplateResponse(name='payment_analysis.html',
                                     context={
                                         'request': request,
                                         'matching': all_pa,
                                     }
                                     )


@html_router.get('/rates')
def view_all_rates(request: Request):
    rates = service.get_all_rates_for_html()
    return template.TemplateResponse(name='rates.html',
                                     context={
                                         'request': request,
                                         'rates': rates,
                                     }
                                     )


@html_router.get('/rates/change/{pk:int}')
def change_rv_form(request: Request, pk: int):
    rv = []
    rv_list = service.get_rv(with_relation=True, id=pk)
    if rv_list:
        rv = rv_list[0]
    return template.TemplateResponse(name='change_rv_form.html',
                                     context={
                                         'request': request,
                                         'rv': rv,
                                     }
                                     )


@html_router.post('/rates/change/{pk:int}')
def change_rv(pk: int,
              new_value: int = Form(),
              date: date = Form()):
    try:
        rv_dto = service.get_rv(id=pk)[0]
        rv = RateValueAddDTO(value=new_value, start_date=date, rate_id=rv_dto.rate_id)

        service.change_rv(rv)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    return RedirectResponse('/rates', status_code=status.HTTP_303_SEE_OTHER)
