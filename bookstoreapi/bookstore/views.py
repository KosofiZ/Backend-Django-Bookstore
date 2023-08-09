from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.decorators import action
from bookstore.models import Client, Order, Comment, WishList, ShippingInfo, Book, Tag, Category, Post, BookOrder
from bookstore.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly


#######################################################

from rest_framework.response import Response
from knox import views as knox_views
from knox.models import AuthToken
from django.contrib.auth import login, logout
# from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.viewsets import ViewSetMixin  




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserExcerptSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# class CreateUserAPI(CreateAPIView):
#     queryset = Client.objects.all()
#     serializer_class = CreateUserSerializer
#     permission_classes = (AllowAny,)

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserExcerptSerializer(user, context=self.get_serializer_context()).data            
        })
    
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserExcerptSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# class UpdateUserAPI(UpdateAPIView):
#     queryset = Client.objects.all()
#     serializer_class = UpdateUserSerializer


class AuthenticationViewSet(viewsets.ModelViewSet):

    permission_classes = (AllowAny, )
    queryset = Client.objects.all()
    serializer_class = LoginSerializer

    

    @action(detail=False, methods=["POST"])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["POST"])
    def logout(self, request):
         if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
         else:
            return Response({'message': 'User is not authenticated.'}, status=status.HTTP_400_BAD_REQUEST)

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