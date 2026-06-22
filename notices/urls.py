from django.urls import path
from .views import NoticeListView, NoticeDetailView

app_name = 'notices'
urlpatterns = [
    path('', NoticeListView.as_view(), name='notice_list'),
    path('<int:pk>/', NoticeDetailView.as_view(), name='notice_detail'),
]
