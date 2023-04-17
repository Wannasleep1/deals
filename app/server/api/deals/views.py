from collections import Counter
from itertools import chain

from django.conf import settings
from django.contrib.postgres.aggregates import StringAgg
from django.core.cache import cache
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import views
from rest_framework.decorators import api_view, schema, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from server.api.deals.schemas import process_deal_schema
from server.api.deals.serializers import CustomerListSerializer
from server.api.deals.utils import process_deals_csv
from server.apps.deals.models import Customer


@api_view(['POST'])
@schema(process_deal_schema)
@parser_classes([MultiPartParser])
def process_deals(request: Request) -> Response:
    """
    View-функция для обработки файла со сделками в формате csv и сохранения результатов в БД.
    """

    data = request.data

    if not data:
        result = ('Error', 'Не передан файл', 400)
    elif len(data) > 1:
        result = ('Error', 'Передано много файлов', 400)
    else:
        file = list(data.values())[0]
        result = process_deals_csv(file)

    # Очищаем кэш
    cache.clear()

    status, details, status_code = result

    return Response({'Status': status, 'Desc': details}, status=status_code)


class CustomerView(views.APIView):
    """
    View для работы с данными покупателей.

    get:
    Получить список из 5 покупателей потративших больше всего денег.

    """

    serializer_class = CustomerListSerializer

    @method_decorator(cache_page(settings.CACHE_TTL))
    def get(self, request: Request) -> Response:

        # Сразу получаем объекты со всеми необходимыми данными
        qs = Customer.objects.annotate(
            spent_money=Sum('deal__total'),
            bought_gems=StringAgg('deal__gem', delimiter=','),
        ).order_by('-spent_money')[:5]

        # Составляем список камней с учётом их появления у разных покупателей
        consumers_gems = list(chain.from_iterable(
            set(el.bought_gems.split(',')) for el in qs
        ))
        gems_counter = Counter(consumers_gems)

        data = self.serializer_class(qs, many=True, context={'gems_counter': gems_counter}).data

        return Response({'response': data}, status=200)
