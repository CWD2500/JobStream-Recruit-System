from logging import DEBUG
from django.contrib import admin
from django.urls import path , include 
from django.conf import settings
from Job.settings import MEDIA_ROOT   , MEDIA_URL 
from django.conf.urls import static
from django.conf.urls.static import static  


urlpatterns = [

    # path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),

    # path('', include('admin_material.urls')),

    path('account/' , include('Account.urls')),
    path('' , include('jobView.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if not DEBUG:
#     urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)