from django.urls import path
from views.views_user import home, user_login, user_signup, user_logout, profile_edit, password_change, profile_delete, profile_view
from views.product_view import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
from views.category_view import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    # URLs pour les utilisateurs
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('password/change/', password_change, name='password_change'),
    path('profile/delete/', profile_delete, name='profile_delete'),
    path('profile/', profile_view, name='profile'),
    # URLs pour les produits
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    # URLs pour les catégories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]