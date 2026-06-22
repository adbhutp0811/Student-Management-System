from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from accounts.views import CollegeHomeView, DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CollegeHomeView.as_view(), name='college_home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('students/', include('students.urls', namespace='students')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('results/', include('results.urls', namespace='results')),
    path('clubs/', include('clubs.urls', namespace='clubs')),
    path('fees/', include('fees.urls', namespace='fees')),
    path('notices/', include('notices.urls', namespace='notices')),
    path('timetable/', include('timetable.urls', namespace='timetable')),
    path('library/', include('library.urls', namespace='library')),
    path('events/', include('events.urls', namespace='events')),
    path('placements/', include('placements.urls', namespace='placements')),
    path('hostel/', include('hostel.urls', namespace='hostel')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
