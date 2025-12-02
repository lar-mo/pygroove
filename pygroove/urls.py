from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('music.urls')),  # <-- points to your app
]

# Serve media files in both development and production
# In production, these are served by WhiteNoise/Gunicorn
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
