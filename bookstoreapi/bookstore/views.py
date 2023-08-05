from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from bookstore.models import Client, Order, Comment, WishList, ShippingInfo, Book, Tag, Category, Post, BookOrder
from bookstore.serializers import *
from django.http import  JsonResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly


#######################################################


from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt



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
    #permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=False, methods=["POST"])
    def add_to_cart(self, request):
        # user = request.user
        user = Client.objects.first()
        book_id = request.data.get('book_id', 0)
        print("Book id:", book_id)
        if book_id is None:
            return Response({'status': "Book ID not provided."}, status=400)
        else:
            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                return Response({'status': "No such book found."}, status=400)
            
        print("book:", book)
        cart_item, created = Cart.objects.get_or_create(user=user)
        cart_item.books.add(book)
        return Response({'status': 'Book added to cart successfully'})

""" 
@csrf_exempt
@api_view(['POST'])
def add_to_cart(request):
    if request.method == 'POST':
            book_id = request.POST.get('bookId')
            if book_id is None:
             return Response({'status': "Book ID not provided."}, status=400)
            
            book_id = int(book_id)
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
    
    return Response({'status': 'Book added to cart successfully'})
 """



        
    
    





