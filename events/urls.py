from django.urls import path
from .views import EventListView, EventDetailView

app_name = 'events'
urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
]
