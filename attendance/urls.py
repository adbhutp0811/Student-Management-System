from django.urls import path
from .views import (
    AttendanceHistoryView,
    AttendanceSummaryView,
    GetStudentsForClassView,
    MarkAttendanceView,
    SaveAttendanceView,
)

app_name = 'attendance'

urlpatterns = [
    path('mark/', MarkAttendanceView.as_view(), name='mark'),
    path('api/get-students/<int:class_id>/', GetStudentsForClassView.as_view(), name='get_students'),
    path('api/save/', SaveAttendanceView.as_view(), name='save'),
    path('history/', AttendanceHistoryView.as_view(), name='history'),
    path('summary/', AttendanceSummaryView.as_view(), name='summary'),
]
