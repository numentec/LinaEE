from django.db import models
from django.contrib.auth import get_user_model
# from crum import get_current_user
from ..core.models import Common, Cia

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

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField("Order Name", max_length=100, blank=True, null=True)
    ciaext = models.CharField("External cia", max_length=10, default='01')
    customer_id = models.CharField("Customer ID", max_length=25, default='0')
    customer_name = models.CharField("Customer Name", max_length=100, default='X customer', null=True)
    customer_email = models.CharField("Customer Email", max_length=100, blank=True, null=True)
    customer_cel = models.CharField("Customer Cell", max_length=100, blank=True, null=True)
    sendto = models.CharField("Send to", max_length=300, blank=True, null=True)
    sendcc = models.CharField("With cc", max_length=300, blank=True, null=True)
    subject = models.CharField("Subject", max_length=100, default='Order')
    saleref = models.CharField("Seller Ref", max_length=100, blank=True, null=True)
    delivery_to = models.CharField("Delivery To", max_length=300, blank=True, null=True)
    carrier_tag = models.CharField("Carrier Tag", max_length=100, blank=True, null=True)
    link = models.CharField("Link", max_length=200, default='/', null=True)
    perm = models.CharField("Permiso", max_length=50, blank = True, help_text='Permiso de acceso relacionado')
    source = models.CharField('Source', max_length=7, choices=SOURCE_CHOICES, default='cart')
    discount_percentage = models.DecimalField("Discount Percentage", max_digits=5, decimal_places=2, default=0.00)
    subtotal = models.DecimalField("Subtotal", max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField("Discount", max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField("Tax", max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField("Total", max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField("Notes", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.sendto:  # Si sendto está vacío o es None
            self.sendto = self.customer_email
        super(ExtOrderMaster, self).save(*args, **kwargs)

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

    def __str__(self):
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


class SaleAppSettings(Common):

    class EmailPolicy(models.TextChoices):
        AUTO = "auto", "Automatic send order"
        ASK = "ask", "Ask before sending order"
        NEVER = "never", "Do not send order"

    class EmailAttachments(models.TextChoices):
        PDF = "pdf", "PDF only"
        XLSX = "xlsx", "Excel only"
        BOTH = "both", "PDF and Excel"

    company = models.OneToOneField(
        Cia,
        on_delete=models.CASCADE,
        related_name="saleapp_settings",
    )

    email_policy = models.CharField(
        max_length=10,
        choices=EmailPolicy.choices,
        default=EmailPolicy.ASK,
    )

    email_attachments = models.CharField(
        max_length=5,
        choices=EmailAttachments.choices,
        default=EmailAttachments.PDF,
    )

    email_include_images = models.BooleanField("Include images", default=False)

    @staticmethod
    def attachment_types_for(attachments):
        """Tipos de archivo (renderers de send_order_email) para una opción de adjuntos"""
        if attachments == SaleAppSettings.EmailAttachments.BOTH:
            return ['pdf', 'xlsx']
        return [attachments]

    @property
    def attachment_types(self):
        return self.attachment_types_for(self.email_attachments)

    @classmethod
    def for_company(cls, cia):
        obj, _ = cls.objects.get_or_create(company=cia)
        return obj

    @staticmethod
    def resolve_company(cia_id=None, user=None):
        """Cia indicada -> Cia del usuario -> Cia predeterminada"""
        if cia_id and str(cia_id).isdigit():
            cia = Cia.objects.filter(pk=cia_id).first()
            if cia:
                return cia
        if user is not None and getattr(user, 'cia_id', None):
            return user.cia
        return Cia.objects.filter(default=True).first() or Cia.objects.get(pk=Cia.DEFAULT_PK)

    def __str__(self):
        return "SaleApp settings - {}".format(self.company)

    class Meta:
        db_table = 'saleapp_settings'
        verbose_name = 'SaleAppSettings'
        verbose_name_plural = 'SaleAppSettings'
