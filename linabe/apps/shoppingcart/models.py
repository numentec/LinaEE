from django.db import models
from django.contrib.auth import get_user_model
# from crum import get_current_user
from ..core.models import Common

LinaUserModel = get_user_model()


class ExtOrderMaster(Common):
    """
    Saving master data for externally generated orders.
    (i.e. External Shoppingcart).
    """

    SOURCE_CHOICES = [
        ('cart', 'Shoppingcart'),
        ('erp', 'ERP'),
        ('clawiki', 'Clawiki'),
    ]

    ciaext = models.CharField("External cia", max_length=10, default='01')
    customer_id = models.CharField("Customer ID", max_length=25, default='0')
    customer_name = models.CharField("Customer Name", max_length=25, default='X customer', null=True)
    customer_email = models.CharField("Customer Email", max_length=100, null=True)
    customer_cel = models.CharField("Customer Cell", max_length=15, null=True)
    sendto = models.CharField("Send to", max_length=300, null=True)
    sendcc = models.CharField("With cc", max_length=300, null=True)
    subject = models.CharField("Subject", max_length=100, default='Order')
    saleref = models.CharField("Seller Ref", max_length=100, null=True)
    link = models.CharField("Link", max_length=200, default='/', null=True)
    perm = models.CharField("Permiso", max_length=50, blank = True, help_text='Permiso de acceso relacionado')
    source = models.CharField('Source', max_length=7, choices=SOURCE_CHOICES, default='cart')
    discount_percentage = models.DecimalField("Discount Percentage", max_digits=5, decimal_places=2, default=0.00)
    subtotal = models.DecimalField("Subtotal", max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField("Discount", max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField("Tax", max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField("Total", max_digits=10, decimal_places=2, default=0.00)

    # def save(self, *args, **kwargs):
    #     user = get_current_user()
    #     if user and not user.pk:
    #         user = None
    #     if not self.pk:
    #         self.created_by = user
    #     self.modified_by = user
    #     super(ExtOrderMaster, self).save(*args, **kwargs)

    class Meta:
        db_table = 'cart_extorder_master'
        verbose_name = 'CartExtOrderMaster'
        verbose_name_plural = 'CartExtOrdersMasters'

    def __str_(self):
        return "External order {} - {} - {}".format(self.id, self.created_at, self.created_by)


class ExtOrderItem(models.Model):
    """
    Saving detail data for external orders.
    Items for ExtOrderMaster class
    """

    extorder = models.ForeignKey(ExtOrderMaster, on_delete=models.CASCADE, related_name='items')
    sku = models.CharField("SKU", max_length=25)
    name = models.CharField("Product Name", max_length=100)
    quantity = models.PositiveIntegerField("Quantity")
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField("Discount Percentage", max_digits=5, decimal_places=2, default=0.00)
    discount = models.DecimalField("Discount", max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField("Tax", max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField("Total", max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'cart_extorder_item'
        verbose_name = 'CartExtOrderItem'
        verbose_name_plural = 'CartExtOrdersItems'

    def __str__(self):
        return "Items for order {} - Product {}".format(self.extorder.id, self.sku)
