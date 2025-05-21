from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from user.models import Product, Category
from django.http import HttpResponseForbidden

from django.views.generic import ListView
from user.models import Product

# user/views.py
from django.views.generic import ListView
from user.models import Product, Category
from django.db.models import Q

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'  # Assurez-vous que c'est correct
    context_object_name = 'products'
    paginate_by = 12  # Pour la pagination

    def get_queryset(self):
        queryset = Product.objects.all()
        search_query = self.request.GET.get('search', '')
        category_id = self.request.GET.get('category', '')

        if search_query:
            queryset = queryset.filter(
                Q(pro_name__icontains=search_query) |
                Q(pro_desc__icontains=search_query)
            )

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    template_name = 'products/product_create.html'
    fields = ['pro_name', 'pro_desc', 'pro_price', 'category','image']
    success_url = reverse_lazy('product_list')

    def test_func(self):
        return hasattr(self.request.user, 'roles') and self.request.user.roles.role_name == 'admin'

    def handle_no_permission(self):
        return HttpResponseForbidden("Vous n'avez pas la permission d'ajouter un produit.")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Produit ajouté avec succès.")
        return super().form_valid(form)

from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from user.models import Product
from user.forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin

# user/views.py
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from user.models import Product
from user.forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'  # Template utilisé pour la création et la mise à jour
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        # Restreindre les produits à ceux de l'utilisateur connecté
        return Product.objects.filter(user=self.request.user)

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user or (hasattr(self.request.user, 'roles') and self.request.user.roles.role_name == 'admin')

    def handle_no_permission(self):
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer ce produit.")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Produit supprimé avec succès.")
        return super().delete(request, *args, **kwargs)