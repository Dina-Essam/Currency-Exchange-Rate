# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand
import random
import json, requests

# python manage.py seed --mode=refresh
from api.models import Currency, ExchangeRate

""" Clear all data and creates currencies """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    Currency.objects.all().delete()


def create_currencies():
    """Retrive Currencies from api.frankfurter and add to database"""
    url = 'https://api.frankfurter.app/currencies'
    response = requests.get(url)
    result = response.json()
    for symbol, currency in result.items():
        currency = Currency(symbol=symbol, name=currency)
        currency.save()
    url = "https://api.frankfurter.app/2020-01-01..2020-01-31"
    response = requests.get(url)
    result = response.json()
    from_currency = Currency.objects.get(symbol=result['base'])
    for date in result['rates']:
        for symbol in result['rates'][date]:
            to_currency = Currency.objects.get(symbol=symbol)
            rate = ExchangeRate(To=to_currency,From=from_currency,date=date,rate=result['rates'][date][symbol])
            rate.save()



def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    create_currencies()
