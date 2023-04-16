from django.contrib import admin

from server.apps.deals.models import Customer, Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    fields = [
        'customer',
        'gem',
        'total',
        'quantity',
        'date',
    ]
    list_display = fields
    ordering = ['-date']
    list_select_related = ['customer']


admin.site.register(Customer)
