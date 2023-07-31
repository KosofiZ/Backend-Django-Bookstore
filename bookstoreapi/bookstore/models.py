from datetime import timezone
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from bookstore import settings as bookstore_settings



class WishList(models.Model):
    books = models.ManyToManyField("Book", verbose_name=_("Books"), blank=True)
    
    def __str__(self):
        if getattr(self, 'user', None):
            return f"{self.user} wishlist"
        return f"Wishlist {self.id}"
    

class Client(User):

    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )
    
    class Meta(User.Meta):
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")


    phone = models.CharField(_("Phone"), max_length=10, validators=[phone_regex], blank= True  )
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
    image = models.ImageField(_("Image"), upload_to="books/images", null=True, blank=True)
    rating = models.DecimalField(_("Rating"), max_digits=2, decimal_places=1, default=0.0, blank=True)

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
    books = models.ManyToManyField(Book, verbose_name=_("Books"), related_name="orders", through="BookOrder")
    created_at = models.DateTimeField(_("Created_at"),auto_now_add=True)
    status = models.CharField(
        _("Status"), choices=bookstore_settings.ORDER_STATUS_CHOICES,
        default="pending", max_length=32
    )
    ShippingInfo = models.OneToOneField(
        ShippingInfo,
        verbose_name=_("ShippingInfo"),
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Order of {self.user}"
    

class BookOrder(models.Model):
     
    class Meta:
        unique_together = (
            "book", "order"
        )

        verbose_name = _("Book order")
        verbose_name_plural = _("Book order")

    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(_("Quantity"), null=False)

    def __str__(self):
        return f"Order of :{self.book}"

    @classmethod
    def filter_by_order(cls, order):
        return BookOrder.objects.filter(order=order)
    
    @classmethod
    def get_books_per_order(cls, order):
        book_ids = BookOrder.objects.filter(order=order).values_list('book__id', flat=True)
        return Book.objects.filter(
            id__in=book_ids
        )
    
    

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
