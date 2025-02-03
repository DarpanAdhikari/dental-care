from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('frontend.urls')),
    path('accounts/',include('accounts.urls')),
    path('admin/',include('administration.urls')),
    path('doctor/',include('doctors.urls')),
    path('patient/',include('patients.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)