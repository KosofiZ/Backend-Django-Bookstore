from django.urls import path, include
from bookstore import views
from rest_framework import routers
from bookstore.views import  RegistrationAPI, LoginAPI


router = routers.DefaultRouter()
router.register(r'client-users', views.ClientViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'wishlists', views.WishlistViewSet)
router.register(r'shipping-infos', views.ShippingInfoViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'cart', views.CartViewSet)
router.register(r'authentication', views.AuthenticationViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    # path('create-user/', views.CreateUserAPI.as_view()),
    # path('update-user/<int:pk>/', views.UpdateUserAPI.as_view()),
    # path('login/', views.LoginAPIView.as_view()),
    path('register/', RegistrationAPI.as_view()),
    path('login/', LoginAPI.as_view()),
]
