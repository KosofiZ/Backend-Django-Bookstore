from django.contrib import admin
from bookstore.models import *

 
 
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_filter = [
        "published_at", 'user'
    ]

    search_fields = ["title", "content"]

    list_display = [
        "__str__",
        "user",
        "created_at",
        "last_updated_at",
        "get_is_published",
    ]

    def get_is_published(self, instance):
         return instance.published_at is not None
    

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_filter = [
        "author",
    ]

    search_fields = ["title", "author", "description"]

    list_display = [
        "__str__",
        "title",
        "quantity",
        "price",
        "book_available",
    ]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_filter = [
        "first_name", 
    ]

    search_fields = ["first_name", "last_name"]

    list_display = [
        "__str__",
        "first_name",
        "email",
        "phone",
        
        ]
    
    #def full_name(self , instance):
        #return str(instance)


@admin.register(ShippingInfo)
class ShippingInfoAdmin(admin.ModelAdmin):

    list_filter = [
        "country", "city", "state"
    ]

    search_fields = ["city", "state", "country", "phone", "postal_code"]

    list_display = [
        "__str__",
        "city",
        "country",
     
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_filter = [
        "name",
    ]

    search_fields = ["name"]

    list_display = [
        "__str__",    
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_filter = [
        "name",
    ]

    search_fields = ["name"]

    list_display = [
        "__str__",    
    ]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_filter = [
        "user",
    ]

    search_fields = ["user"]

    list_display = [
        "__str__",    
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_filter = [
        "user"
    ]

    fields = [
        "user",
        "status",
        "shipping_info",
    ]
     
    filter_horizontal = ["books"]  # For ManyToManyField use filter_horizontal instead of fields
    
    search_fields = ["user", "created_at"]

    list_display = [
        "__str__",
        "user",
        "created_at",
        "status",
        "total_amount",
    ]


    def total_amount(self, obj):
        # Define a method to calculate and display the total amount for each order
        return sum(item.price for item in obj.books.all())


@admin.register(BookOrder)
class BookOrderAdmin(admin.ModelAdmin):

    list_display = [
        "__str__",
        "book",
        "quantity",
    ]

    search_fields = ["book"]

