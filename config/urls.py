from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('', RedirectView.as_view(url=reverse_lazy('web:home'), permanent=True)),
    path('', include('apps.web.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)