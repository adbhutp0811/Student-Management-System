from django.urls import path
from .views import (
    ClassResultSummaryView,
    GetSubjectsExamView,
    ManageResultsView,
    ReportCardView,
    SaveResultsView,
)

app_name = 'results'

urlpatterns = [
    path('manage/', ManageResultsView.as_view(), name='manage'),
    path('api/get-data/', GetSubjectsExamView.as_view(), name='get_data'),
    path('api/save/', SaveResultsView.as_view(), name='save'),
    path('class-summary/', ClassResultSummaryView.as_view(), name='class_summary'),
    path('report-card/<int:pk>/', ReportCardView.as_view(), name='report_card'),
]
