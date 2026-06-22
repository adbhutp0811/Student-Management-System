from django.urls import path
from .views import CompanyListView, PlacementDriveListView, PlacementDriveDetailView

app_name = 'placements'
urlpatterns = [
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('drives/', PlacementDriveListView.as_view(), name='drive_list'),
    path('drives/<int:pk>/', PlacementDriveDetailView.as_view(), name='drive_detail'),
]
