from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
import uuid


class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name

    class Meta:
        indexes = [models.Index(fields=['role_name'])]


class CustomUser(AbstractUser):
    roles = models.ForeignKey(
        'Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Attribuer le rôle 'user' par défaut pour les nouveaux utilisateurs
        if not self.pk and not self.roles:
            role, _ = Role.objects.get_or_create(role_name='user')
            self.roles = role
        super().save(*args, **kwargs)

    def is_admin(self):
        return self.roles and self.roles.role_name == 'admin'

    class Meta:
        indexes = [models.Index(fields=['roles'])]


class Category(models.Model):
    cat_name = models.CharField(max_length=45, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cat_name

    def save(self, *args, **kwargs):
        self.cat_name = self.cat_name.lower()
        super().save(*args, **kwargs)

    class Meta:
        indexes = [models.Index(fields=['cat_name'])]


class Product(models.Model):
    pro_name = models.CharField(max_length=45)
    pro_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    pro_desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products'
    )
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='products'
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # Nouveau champ pour upload #

    def __str__(self):
        return self.pro_name

    class Meta:
        indexes = [models.Index(fields=['user', 'category'])]


class Sale(models.Model):
    sale_code = models.CharField(max_length=45, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='sales'
    )

    def __str__(self):
        return f"Sale {self.sale_code}"

    def save(self, *args, **kwargs):
        if not self.sale_code:
            self.sale_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    class Meta:
        indexes = [models.Index(fields=['sale_code', 'user'])]


class Bill(models.Model):
    qty = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='bills'
    )
    sale = models.ForeignKey(
        'Sale',
        on_delete=models.CASCADE,
        related_name='bills'
    )
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill for {self.product} (Qty: {self.qty})"

    def save(self, *args, **kwargs):
        self.sale_price = self.product.pro_price * self.qty
        super().save(*args, **kwargs)

    @property
    def total(self):
        return self.sale_price

    class Meta:
        indexes = [models.Index(fields=['sale', 'product'])]


class PayMethod(models.Model):
    pay_name = models.CharField(max_length=45, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pay_name

    class Meta:
        indexes = [models.Index(fields=['pay_name'])]


class Payment(models.Model):
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paymethod = models.ForeignKey(
        'PayMethod',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    sale = models.ForeignKey(
        'Sale',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    def __str__(self):
        return f"Payment for {self.sale} via {self.paymethod}"

    class Meta:
        indexes = [models.Index(fields=['sale', 'paymethod'])]



class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')
        indexes = [models.Index(fields=['cart', 'product'])]

    def __str__(self):
        return f"{self.product.pro_name} x {self.quantity}"

    def get_total_price(self):
        return self.product.pro_price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total(self):
        return sum(item.get_total_price() for item in self.cart_items.all())

    class Meta:
        indexes = [models.Index(fields=['user'])]


    def get_total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())