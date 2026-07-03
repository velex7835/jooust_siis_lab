from django.contrib import admin
from django.urls import path
from lab_portal.views import report_issue

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', report_issue, name='report_issue'),
]
