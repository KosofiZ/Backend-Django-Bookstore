from django.urls import path, include
from rest_framework import routers
from django.contrib import admin
from bookstore import views

router = routers.DefaultRouter()
router.register(r'client-users', views.ClientViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'wishlists', views.WishlistViewSet)
router.register(r'shipping-infos', views.ShippingInfoViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('i18n/', include('django.conf.urls.i18n')),
    

]
