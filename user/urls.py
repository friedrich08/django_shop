from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from views.cart_view import download_invoice, update_cart, remove_from_cart

# Vues utilisateur
from views.views_user import home, user_login, user_signup, user_logout, profile_edit, password_change, profile_delete, profile_view

# Vues produit
from views.product_view import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

# Vues catégorie
from views.category_view import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

# Vues panier
from views.cart_view import add_to_cart, cart_view, confirm_payment, payment_success
urlpatterns = [
    # === Utilisateurs ===
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('password/change/', password_change, name='password_change'),
    path('profile/delete/', profile_delete, name='profile_delete'),
    path('profile/', profile_view, name='profile'),

    # === Produits ===
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # === Catégories ===
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # === Panier ===
    
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/confirm/', confirm_payment, name='confirm_payment'),
    path('payment/success/<int:payment_id>/', payment_success, name='payment_success'),
    path('download/invoice/<int:invoice_id>/', download_invoice, name='download_invoice'),
    path('cart/update/<str:action>/<int:cart_item_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),  # ← Ajout ici


]

# Ajout des fichiers médias (images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)