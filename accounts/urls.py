from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView,
    RegisterView,
    StudentLoginView,
    StudentLogoutView,
    StudentPortalView,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('student-login/', StudentLoginView.as_view(), name='student_login'),
    path('student-logout/', StudentLogoutView.as_view(), name='student_logout'),
    path('student-portal/', StudentPortalView.as_view(), name='student_portal'),
]
