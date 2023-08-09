from django.utils.translation import gettext_lazy as _


ORDER_STATUS_CHOICES = (
    ("pending", _("Pending")),
    ("shipping", _("Shipping")),
    ("shipped", _("Shipped")),
)