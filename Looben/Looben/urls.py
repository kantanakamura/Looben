from cgitb import handler
import sre_compile
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import page_not_found, server_error


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('reviews.urls')),
    path('', include('dashboard.urls')),
    path('', include('job.urls')),
    path('', include('blogs.urls')),
    path('', include('questions.urls')),
]

handler404 = page_not_found
handler500 = server_error

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    