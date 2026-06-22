from django.urls import path
from .views import ClubListView, ClubDetailView, ClubApplyView

app_name = 'clubs'
urlpatterns = [
    path('', ClubListView.as_view(), name='club_list'),
    path('<int:pk>/', ClubDetailView.as_view(), name='club_detail'),
    path('<int:pk>/apply/', ClubApplyView.as_view(), name='club_apply'),
]
