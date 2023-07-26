from datetime import timezone
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator



class WishList(models.Model):
    books = models.ManyToManyField("Book", verbose_name=_("Books"), blank=True)
    

    def __str__(self):
        return self.id
    

class Client(User):

    # phone_regex = RegexValidator(
    #     regex=r'^\d{10}$',
    #     message="Phone number must be exactly 10 digits."
    # )
    # put inside phone attribute validators=[phone_regex] 

    class Meta(User.Meta):
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")


    phone = models.CharField(_("Phone"), max_length=10 )
    shipping_info = models.OneToOneField(
        'ShippingInfo', verbose_name=_("Shipping Info"), on_delete=models.PROTECT
        , blank=True, null=True
    )
    wishlist = models.OneToOneField(
        WishList, verbose_name=_("Wishlist"), related_name='user', on_delete=models.PROTECT,
        blank=True
    )

    # def __str__(self):
    #    return f"{self.first_name} {self.last_name}"
       
    
    def __str__(self):
         return str(self.username)   


    def save(self, *args, **kwargs):
        if not hasattr(self, 'wishlist'):
            self.wishlist = WishList.objects.create()
        super().save(*args, **kwargs)


class Category(models.Model):

    class Meta(User.Meta):
            verbose_name = _("Category")
            verbose_name_plural = _("Categories")

    name = models.CharField(_("Name"), max_length=100, blank=False)

    def __str__(self):
            return self.name


class Tag(models.Model):
    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name

    
class Book(models.Model):
    title = models.CharField(_("Title "), max_length=100 ,blank=False) 
    author = models.CharField(_("Author "), max_length=100, default="", blank=False)
    editor = models.CharField(_("Editor "), max_length=100, default="", blank=True)
    description = models.TextField(_("Description"), blank = True)
    quantity = models.PositiveIntegerField(_("Quantity"), default=0, blank=True)
    price = models.DecimalField(_("Price"), max_digits=6, decimal_places=2, null=False, blank=False)
    book_available = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, verbose_name=("Categories"), related_name="books", blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), related_name="books", blank=True)
    image_url = models.CharField(_("imageUrl"), max_length=200, blank=True, null =True)
    rating = models.FloatField(default=0.0)  

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.book_available = self.quantity > 0
        super(Book, self).save(*args, **kwargs)

class ShippingInfo(models.Model):

    class Meta:
        verbose_name = _("Shipping information")
        verbose_name_plural = _("Shipping information")

    name = models.CharField(_("Name"), max_length=50, default="", blank=True)
    address = models.CharField(_("Address"), max_length=255, blank=False)
    city = models.CharField(_("City"), max_length=100, blank=False)
    state = models.CharField(_("State"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal_code"), max_length=20, blank=True)
    country = models.CharField(_("Country"), max_length=255, default="", blank=False)
    phone = models.CharField(_("Phone"), max_length=10, blank=True)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    user = models.ForeignKey(Client, verbose_name=_("User"), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    text = models.TextField(_("Text"), blank=True)
    rating = models.DecimalField(_("Rating"), max_digits=2, decimal_places=1, blank=False)

    def __str__(self):
        return f"{self.user} - {self.book} - {self.rating}"
    

class Order(models.Model):
    user = models.ForeignKey(Client, verbose_name=_("User"), null=True, on_delete=models.SET_NULL)
    books = models.ManyToManyField(Book, verbose_name=_("Books"), related_name="orders")
    created_at = models.DateTimeField(_("Created_at"),auto_now_add=True)
    ShippingInfo = models.OneToOneField(
        ShippingInfo,
        verbose_name=_("ShippingInfo"),
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Order {self.user}"
    

class Post(models.Model):

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = [
            "-published_at", "title"
        ]

    user = models.ForeignKey(User, verbose_name=_("User"), null= True, on_delete=models.SET_NULL, related_name="posts")
    title = models.CharField(_("Title "), max_length=256, blank=False)
    content = models.TextField(_("Content"), blank = True)
    categories = models.ManyToManyField(Category, verbose_name=("Categories"), related_name="posts", blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), related_name="posts", blank=True) 
    created_at = models.DateTimeField(_("Creation date"), auto_now_add=True)
    last_updated_at = models.DateTimeField(_("Last modification date"), auto_now=True)
    published_at = models.DateTimeField(_("Publication date"), null=True, blank=True)
    
    def __str__(self):
        return f"{self.title}"

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def unpublish(self):
        self.published_at = None
        self.save()
