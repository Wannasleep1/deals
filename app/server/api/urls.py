from django.urls import path

from server.api.deals.views import CustomerView, process_deals


app_name = 'api'


urlpatterns = [
    path('customer/', CustomerView.as_view()),
    path('process_deals/', process_deals),
]
