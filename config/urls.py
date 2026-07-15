from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize the Django Admin/Staff Portal Branding
admin.site.site_header = "JOOUST SIIS Staff Portal"
admin.site.site_title = "JOOUST Staff Admin"
admin.site.index_title = "Technical Issue Operations Control"

urlpatterns = [
    # Renamed path from 'admin/' to 'staff/'
    path('staff/', admin.site.urls),
    path('', include('lab_portal.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
