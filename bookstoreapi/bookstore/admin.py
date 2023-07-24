from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Order)


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
        "username", 
    ]

    search_fields = ["username", "first_name", "last_name"]

    list_display = [
        "__str__",
        #"full_name",
        "username",
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