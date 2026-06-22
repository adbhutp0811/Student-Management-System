from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView,
    StudentLoginView,
    StudentLogoutView,
    StudentPortalView,
    ResultPortalView,
    AdmissionsView,
    MandatoryDisclosureView,
    AcademicCalendarView,
    NIRFView,
    ResearchView,
    FacultyView,
    FacultyDetailView,
    SyllabusView,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('student-login/', StudentLoginView.as_view(), name='student_login'),
    path('student-logout/', StudentLogoutView.as_view(), name='student_logout'),
    path('student-portal/', StudentPortalView.as_view(), name='student_portal'),
    path('result-portal/', ResultPortalView.as_view(), name='result_portal'),
    path('admissions/', AdmissionsView.as_view(), name='admissions'),
    path('mandatory-disclosure/', MandatoryDisclosureView.as_view(), name='mandatory_disclosure'),
    path('academic-calendar/', AcademicCalendarView.as_view(), name='academic_calendar'),
    path('nirf/', NIRFView.as_view(), name='nirf'),
    path('research/', ResearchView.as_view(), name='research'),
    path('faculty/', FacultyView.as_view(), name='faculty'),
    path('faculty/<slug:slug>/', FacultyDetailView.as_view(), name='faculty_detail'),
    path('syllabus/', SyllabusView.as_view(), name='syllabus'),
]
