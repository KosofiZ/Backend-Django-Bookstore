from rest_framework import generics
from rest_framework import viewsets
from .models import Client, Order, Comment, WishList, ShippingInfo, Book, Tag, Category, Post
from .serializers import *


#######################################################


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@api_view(['POST'])
def add_to_cart(request):
    book_id = request.data.get('book_id')
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({"message": "Book not found."}, status=404)

    order, _ = Order.objects.get_or_create(user=request.user)
    order.books.add(book)
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=200)
