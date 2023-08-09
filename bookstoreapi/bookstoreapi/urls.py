from django.urls import path, include, re_path
from rest_framework import routers
from django.contrib import admin
from django.contrib.auth import views as auth_views

from knox.views import LogoutView, LogoutAllView
from knox import views as knox_views
#---------------------     ---------------------

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace ='rest_framework')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('bookstore.urls')),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
    path('api/auth/', include('knox.urls'))


]



urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

