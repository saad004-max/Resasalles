from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importer settings
from django.conf.urls.static import static # Importer static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
]

# Ajouter ceci pour servir les fichiers media en mode developpement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)