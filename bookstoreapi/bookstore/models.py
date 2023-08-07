from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings

from bookstore import settings as bookstore_settings


class WishList(models.Model):
    books = models.ManyToManyField("Book", verbose_name=_("Books"), blank=True)
    
    def __str__(self):
        if getattr(self, 'user', None):
            return f"{self.user} wishlist"
        return f"Wishlist {self.id}"
    

# class CustomAccountManager(BaseUserManager):

#     def create_superuser(self, email, user_name, first_name, password, **other_fields):

#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_active', True)

#         if other_fields.get('is_staff') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_staff=True.')
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_superuser=True.')

#         return self.create_user(email, user_name, first_name, password, **other_fields)

#     def create_user(self, email, user_name, first_name, password, **other_fields):

#         if not email:
#             raise ValueError(_('You must provide an email address'))

#         email = self.normalize_email(email)
#         user = self.model(email=email, user_name=user_name,
#                           first_name=first_name, **other_fields)
#         user.set_password(password)
#         user.save()
#         return user

###  I need to change this  to Django knox and keep inheritance to User 
    


class Client(User):

    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )
    
    # class Meta(AbstractBaseUser.Meta):
    #     verbose_name = _("Client")
    #     verbose_name_plural = _("Clients")

      
    email = models.EmailField( _("email"), unique=True)
    user_name = models.CharField(_("user_name"),max_length=150, unique=True, null=False, blank=False)
    first_name = models.CharField(_("first_name"),max_length=150, blank=True, null= True)
    last_name = models.CharField(_("last_name"), max_length=150, blank=True, null= True)

    phone = models.CharField(_("Phone"), max_length=10, validators=[phone_regex], blank= True )
    shipping_info = models.OneToOneField(
        'ShippingInfo', verbose_name=_("Shipping Info"), on_delete=models.PROTECT
        , blank=True, null=True
    )
    wishlist = models.OneToOneField(
        WishList, verbose_name=_("Wishlist"), related_name='user', on_delete=models.PROTECT,
        blank=True
    )

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name
 

    def __str__(self):
         return str(self.user_name)   


    def save(self, *args, **kwargs):
        if not hasattr(self, 'wishlist'):
            self.wishlist = WishList.objects.create()
        super().save(*args, **kwargs)


# class Client(User):

#     phone_regex = RegexValidator(
#         regex=r'^\d{10}$',
#         message="Phone number must be exactly 10 digits."
#     )
    
#     class Meta(User.Meta):
#         verbose_name = _("Client")
#         verbose_name_plural = _("Clients")


#     phone = models.CharField(_("Phone"), max_length=10, validators=[phone_regex], blank= True )
#     shipping_info = models.OneToOneField(
#         'ShippingInfo', verbose_name=_("Shipping Info"), on_delete=models.PROTECT
#         , blank=True, null=True
#     )
#     wishlist = models.OneToOneField(
#         WishList, verbose_name=_("Wishlist"), related_name='user', on_delete=models.PROTECT,
#         blank=True
#     )

    
#     def get_full_name(self):
#         return self.first_name

#     def get_short_name(self):
#         return self.first_name
 

#     def __str__(self):
#          return str(self.username)   


#     def save(self, *args, **kwargs):
#         if not hasattr(self, 'wishlist'):
#             self.wishlist = WishList.objects.create()
#         super().save(*args, **kwargs)


class Category(models.Model):

    class Meta(AbstractBaseUser.Meta):
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
    image = models.ImageField(_("Image"), upload_to="bookstoreapi/books/images", null=True, blank=True)
    rating = models.DecimalField(_("Rating"), max_digits=2, decimal_places=1, default=0.0, blank=True)
    year_published = models.CharField(_("Year of publication"), max_length=4,blank =True)
    pages = models.CharField(_("Pages"), max_length=5, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.book_available = self.quantity > 0
        super(Book, self).save(*args, **kwargs)
 
"""     
     @property
    def get_image_url(self) -> str:
      if self.image_file and hasattr(self.image_file, 'url'):
         return f"http://localhost:8000{self.image_file.url}"
          
 """
 
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


class Cart(models.Model):

    user = models.OneToOneField(Client, verbose_name=_("User"), null=True,  default="", on_delete=models.SET_NULL)
    books = models.ManyToManyField(Book, verbose_name=_("Books"), blank= True)
    created_at = models.DateTimeField(_("Created_at"),auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user}"
    


class Order(models.Model):

    user = models.ForeignKey(Client, verbose_name=_("User"), on_delete=models.PROTECT)
    books = models.ManyToManyField(Book, verbose_name=_("Books"), related_name="orders", through="BookOrder")
    shipping_info = models.ForeignKey(
        ShippingInfo, verbose_name=_("Shipping Infos"), related_name="orders",
        on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(_("Created_at"), auto_now_add=True)
    status = models.CharField(
        _("Status"), choices=bookstore_settings.ORDER_STATUS_CHOICES,
        default="pending", max_length=32
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL , verbose_name=_("User"), null= True, on_delete=models.SET_NULL, related_name="posts")
    # user = models.ForeignKey(User, verbose_name=_("User"), null= True, on_delete=models.SET_NULL, related_name="posts")

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
        self.published_at = timezone.now() # type: ignore
        self.save()

    def unpublish(self):
        self.published_at = None
        self.save()
