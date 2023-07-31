from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from .models import Client, Order, Comment, WishList, ShippingInfo, Book, Tag, Category, Post, BookOrder
from .serializers import *
from django.http import  JsonResponse


#######################################################


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

def get_object (self, queryset=None ,**kwargs):
    item = self.kwargs.get('pk')
    return get_object_or_404(Book, title =item)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


def add_to_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        
        
        
        try:
            book = Book.objects.get(pk=book_id)
            order, created = Order.objects.get_or_create( status='pending')
            BookOrder.objects.create(order=order, book=book, quantity=1)
            return JsonResponse({'message': 'Book added to cart successfully.'})
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found.'}, status=404)
        

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

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



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer






