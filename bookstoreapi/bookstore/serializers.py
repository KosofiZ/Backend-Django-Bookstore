from rest_framework import serializers

from bookstore.models import Client, Order, Comment, WishList, ShippingInfo, Book, Tag, Category, Post, Cart
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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
        

class UserExcerptSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
        ]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [ 
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'required': True}
        }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data.get('email', '')
        if Client.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "email": 'User with this email already exists.'
            })
        return validated_data

    def create(self, validated_data):
        user = Client.objects.create_user(**validated_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email',  'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

#     def validate(self, attrs):
#         email = attrs.get('email').lower()
#         password = attrs.get('password')

#         if not email or not password:
#             raise serializers.ValidationError("Please give both email and password.")

#         if not Client.objects.filter(email=email).exists():
#             raise serializers.ValidationError('Email does not exist.')

#         user = authenticate(request=self.context.get('request'), email=email,
#                             password=password)
#         if not user:
#             raise serializers.ValidationError("Wrong Credentials.")

#         attrs['user'] = user
#         return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")



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

    serialized_tags = TagSerializer(many=True, source="tags")
    
    class Meta:
        model = Book
        fields = [ 
            'id',
            'title',
            'author',
            'editor',
            'description',
            'image_url',
            'quantity',
            'price',
            'year_published',
            'rating',
            'tags',
            'serialized_tags',
            'pages',
        ]


        
class OrderSerializer(serializers.ModelSerializer):

    books = BookSerializer(many=True, read_only=True)

    #books = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [ 
            'id',
            'books',
            'created_at',
            'ShippingInfo',
        ]

        #fields = '__all__'

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart

        fields = [ 
            'id',
            'user',
            'books',
            'created_at',
        ]

        extra_kwargs  = {  "created_at": {"format": "%Y/%d/%m %H:%M"}  }


class PostSerializer(serializers.ModelSerializer):

    user_data = UserExcerptSerializer(source="user")
    #user_data = serializers.SerializerMethodField()
    
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
