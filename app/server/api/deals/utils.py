import csv
import io
from datetime import datetime
from itertools import chain

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction, IntegrityError

from server.apps.deals.models import Customer, Deal


def process_deals_csv(file: InMemoryUploadedFile) -> tuple[str, str, int]:
    """
    Функция для парсинга файла в формате csv и сохранения данных в БД.

    :param InMemoryUploadedFile file: файл
    :return: кортеж со статусом обработки, текстом результата и статусом запроса
    :rtype: tuple

    """

    # Поля, которые должны присутствовать в файле
    fields: tuple = ('customer', 'item', 'total', 'quantity', 'date')

    # Обработка ситуации с неправильным форматом
    try:
        csv_reader: csv.DictReader = csv.DictReader(io.StringIO(file.read().decode()))
    except UnicodeDecodeError:
        return 'Error', 'Неправильный формат файла', 400

    # Нет требуемых полей (файл должен обязательно содержать необходимые поля)
    if set(fields) - (set(fields) & set(csv_reader.fieldnames)):
        return 'Error', 'Отсутствуют необходимые поля', 400

    customers: dict = {}
    deals_to_create: dict = {}

    # Обрабатываем поля файла
    for row in csv_reader:
        username: str = row['customer']

        if username not in customers:
            customers[username] = Customer(username=username)

        # Проверка корректности типов данных
        try:
            deal_dt: datetime = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S.%f')
            deal = Deal(
                customer=None,
                gem=row['item'],
                total=int(row['total']),
                quantity=int(row['quantity']),
                date=deal_dt,
            )
        except (TypeError, ValueError):
            return 'Error', 'Одно из полей содержит некорректный тип или формат данных', 400

        if username not in deals_to_create:
            deals_to_create[username] = [deal]
        else:
            deals_to_create[username].append(deal)

    # Операции с базой данных обернём в транзакцию, чтобы при ошибке часть данных не осталась не сохранённой
    try:
        with transaction.atomic():

            # Очищаем БД от прежних записей, сделки удалятся каскадом
            Customer.objects.all().delete()

            # Создаём покупателей
            customers_created = Customer.objects.bulk_create(customers.values())

            # Добавляем вновь созданные объекты покупателей в сделки
            for customer in customers_created:
                for deal in deals_to_create[customer.username]:
                    deal.customer = customer

            # Создаём сделки
            Deal.objects.bulk_create(chain.from_iterable(deals_to_create.values()))

    except IntegrityError:
        return 'Error', 'Ошибка при попытке загрузить данные в базу данных', 400
    from django.db import connection
    print(connection.queries)

    return 'Ok', 'Данные обработаны',  200
