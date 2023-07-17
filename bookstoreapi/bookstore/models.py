from django.db import models

# Create your models here.

class ClientUser(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField((""), max_length=254)
    phone = models.CharField(max_length=10)
    shipping_info = models.OneToOneField('ShippingInfo', on_delete=models.CASCADE)
    #wishlist = models.ManyToManyField(Book, related_name='wishlists')

    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    price = models.FloatField()
    

    def __str__(self):
        return self.title
    

class ShippingInfo(models.Model):
    name = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255, default="")
    
    # Add more fields as per your requirement

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return self.text[:50]
    

class Order(models.Model):
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    created_at = models.DateTimeField(auto_now_add=True)
    ShippingInfo = models.OneToOneField(
        ShippingInfo,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Order {self.id}"
    


class Category(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name
    
class WishList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)


    def __str__(self):
        return self.name
    
    

    