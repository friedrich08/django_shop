from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, Category, Product, Sale, Bill, PayMethod, Payment


# Personnaliser l'affichage de CustomUser dans l'admin
class CustomUserAdmin(UserAdmin):
    # Ajouter le champ 'roles' dans le formulaire de modification
    fieldsets = UserAdmin.fieldsets + (
        ('Rôles', {'fields': ('roles',)}),
    )
    # Afficher le rôle dans la liste des utilisateurs
    list_display = ['username', 'email', 'roles', 'is_staff']
    list_filter = ['roles']
    search_fields = ['username', 'email']

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_name']
    search_fields = ['role_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cat_name', 'created_at']
    search_fields = ['cat_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pro_name', 'pro_price', 'category', 'user']
    list_filter = ['category', 'user']
    search_fields = ['pro_name']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_code', 'user', 'created_at']
    list_filter = ['user']
    search_fields = ['sale_code']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['product', 'qty', 'sale_price', 'sale']
    list_filter = ['sale']
    search_fields = ['product__pro_name']


@admin.register(PayMethod)
class PayMethodAdmin(admin.ModelAdmin):
    list_display = ['pay_name']
    search_fields = ['pay_name']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['sale', 'paymethod', 'amount', 'created_at']
    list_filter = ['paymethod']
    search_fields = ['sale__sale_code']