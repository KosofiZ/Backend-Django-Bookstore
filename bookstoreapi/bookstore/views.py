from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from .models import Client, Order, Comment, WishList, ShippingInfo, Book, Tag, Category, Post, BookOrder
from .serializers import *
from django.http import  JsonResponse


#######################################################


from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response



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




""" def add_to_cart(request, book_id):
    try:
        Cart.user = User(Client)
        books = Book.objects.get(pk=book_id)
        cart = Cart.objects.create(user= request.user, books=books)
        cart.save()
        return Response({"message": "Book added to cart successfully"})
    except Book.DoesNotExist:
        return Response({"message": "Book not found"}, status=404)
    except Cart.DoesNotExist:
        return Response({"message": "Cart not found"}, status=404) """

def add_to_cart(request):
    if request.method == 'POST':
            book_id = int(request.POST.get('bookId'))
            book_check = Book.objects.get(id = book_id)
            if(book_check):
                if(Cart.objects.filter(user = request.user.id, bookId = book_id)):
                    return JsonResponse({'status':"Book Already in Cart"})
                else:
                    book_qty = int(request.POST.get('bookQty'))

                    if book_check.quantity >= book_qty : 
                        Cart.objects.create(user = request.user, bookId= book_id, bookQty = book_qty)
                        return JsonResponse({'status': "Book added succesfully"})
                    
                    else:
                        return JsonResponse({'status':"Only" + str(book_check.quantity) + "quantity available"})
            else:
                return JsonResponse({'status': "No such book found"})
        
    
    





