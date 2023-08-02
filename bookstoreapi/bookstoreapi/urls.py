from django.urls import path, include
from rest_framework import routers
from django.contrib import admin
from bookstore import views
from bookstore.views import add_to_cart
from django.contrib.auth import views as auth_views

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
router.register(r'cart', views.CartViewSet)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('i18n/', include('django.conf.urls.i18n')),
    # path('api/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    # path('api/books/<int:book_id>/', views.get_book_detail, name='get_book_detail'),
    path('api/books/<int:book_id>/add-to-cart/', add_to_cart, name='add-to-cart'),
   

    

]

