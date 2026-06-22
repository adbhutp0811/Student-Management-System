from django.urls import path
from .views import HostelListView, HostelDetailView

app_name = 'hostel'
urlpatterns = [
    path('', HostelListView.as_view(), name='hostel_list'),
    path('<int:pk>/', HostelDetailView.as_view(), name='hostel_detail'),
]
