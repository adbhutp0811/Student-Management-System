from django.urls import path
from .views import FeeListView

app_name = 'fees'
urlpatterns = [
    path('', FeeListView.as_view(), name='fee_list'),
]
