from rest_framework import viewsets
from .models import ClientUser, Order, Comment, WishList, ShippingInfo, Book, Tag, Category
from .serializers import ClientUserSerializer, OrderSerializer, CommentSerializer, WishlistSerializer, ShippingInfoSerializer, BookSerializer, TagSerializer, CategorySerializer

class ClientUserViewSet(viewsets.ModelViewSet):
    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishlistSerializer

class ShippingInfoViewSet(viewsets.ModelViewSet):
    queryset = ShippingInfo.objects.all()
    serializer_class = ShippingInfoSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
