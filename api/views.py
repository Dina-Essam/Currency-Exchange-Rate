from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import ExchangeRateSerializer
from .helpers import helper_functions
# Create your views here.


@api_view(['GET'])
def exchangeRate(request):
    from_currency = request.query_params.get('from')
    to_currency = request.query_params.get('to')
    date = request.query_params.get('date')
    rate = helper_functions.get_exchange_rate(from_currency, to_currency, date)
    serializer = ExchangeRateSerializer(rate, many=False)
    return Response(serializer.data)
