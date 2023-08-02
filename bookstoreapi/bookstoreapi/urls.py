from django.urls import path, include
from rest_framework import routers
from django.contrib import admin
from bookstore import views
from bookstore.views import add_to_cart
from django.contrib.auth import views as auth_views
# ---------------------     ---------------------
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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
router.register(r'add_to_cart', views.CartViewSet)








urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace ='rest_framework')),
    path('i18n/', include('django.conf.urls.i18n')),
    # path('api/books/<int:book_id>/', views.get_book_detail, name='get_book_detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   

    

]

