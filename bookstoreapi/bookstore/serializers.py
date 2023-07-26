from rest_framework import serializers
from bookstore.models import Client, Order, Comment, WishList, ShippingInfo, Book, Tag, Category, Post
from django.contrib.auth.models import User


class UserExcerptSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
        ]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [ 
            'id',
            'username',
            'email',
        ]




class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [ 
            'id',
            'client',
            'book',
            'text',
        ]


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = [ 
            'id',
            'books',
        ]


class ShippingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingInfo
        fields = [ 
            'id',
            'name',
            'city',
            'country',
            ]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [ 
            'id',
            'title',
            'image_url',
            'author',
            'quantity',
            'price',
        ]
        
class OrderSerializer(serializers.ModelSerializer):

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [ 
            'id',
            'books',
            'created_at',
        ]



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [ 
            'id',
            'name',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ 
            'id',
            'name',
        ]
        

class PostSerializer(serializers.ModelSerializer):

    # user_data = UserExcerptSerializer(source="user")
    user_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [ 
            'id',
            'user',
            'user_data',
            'title',
            'categories',
            'content',
            'created_at',
            'last_updated_at',
            'published_at'
        ]
        # read_only_fields = [
        #     "user_data"
        # ]
        extra_kwargs  = {
            "user": {
                "write_only": True
            },
            "created_at": {"format": "%Y/%d/%m %H:%M"},
            "last_updated_at": {"format": "%Y/%d/%m %H:%M"},
            "published_at": {"format": "%Y/%d/%m %H:%M"},
        }
    
    def get_user_data(self, object):
        return UserExcerptSerializer(instance=object.user).data
