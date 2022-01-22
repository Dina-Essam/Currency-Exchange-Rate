import requests
from dateutil.relativedelta import relativedelta, FR
from rest_framework import status

from api.models import ExchangeRate, Currency
from django.utils.dateparse import parse_date

from utils.customvalidation import CustomValidation


def check_currency(symbol):
    try:
        return Currency.objects.get(symbol=symbol)
    except Currency.DoesNotExist:
        raise CustomValidation('Invalid Currency Symbol', 'message',
                               status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def get_from_frankfurter(from_currency, to_currency, date):
    url = "https://api.frankfurter.app/" + date + "?from=" + from_currency.symbol + "&to" + to_currency.symbol
    response = requests.get(url)
    result = response.json()
    rate = ExchangeRate(To=to_currency, From=from_currency, date=result['date'],
                        rate=result['rates'][to_currency.symbol])
    rate.save()
    return rate


def check_day_weekend(date):
    try:
        date = parse_date(date)
    except ValueError as ex:
        raise CustomValidation(ex.__str__(), 'message',
                               status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if date.weekday() in [5, 6]:
        date = date + relativedelta(weekday=FR(-1))
    return date.__str__()


class helper_functions:

    @staticmethod
    def get_exchange_rate(from_currency, to_currency, date):
        from_currency_object = check_currency(from_currency)
        to_currency_object = check_currency(to_currency)
        date = check_day_weekend(date)
        if from_currency == to_currency:
            return ExchangeRate(To=to_currency_object, From=from_currency_object, date=date,
                                rate=1)
        try:
            return ExchangeRate.objects.get(date=date, To=to_currency_object, From=from_currency_object)
        except ExchangeRate.DoesNotExist:
            return get_from_frankfurter(from_currency_object, to_currency_object, date)
