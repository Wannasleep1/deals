from django.db import models


class Customer(models.Model):

    username = models.CharField(max_length=100, verbose_name='Имя пользователя')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Deal(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    gem = models.CharField(max_length=50, verbose_name='Драгоценный камень')
    total = models.PositiveIntegerField(verbose_name='Сумма')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество (шт)')
    date = models.DateTimeField(verbose_name='Время совершения сделки')

    def __str__(self):
        return f'Покупатель: {self.customer.username}; Дата сделки: {self.date}'

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
