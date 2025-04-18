from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from user.models import Category  # Import the Category model
from user.forms import CategoryForm  # Import the form for categories

# Category List View
class CategoryListView(ListView):
    model = Category
    template_name = 'ad/category_list.html'  # Template for listing categories
    context_object_name = 'categories'  # Name of the context variable in the template
    paginate_by = 10  # Optional: Add pagination if there are many categories

    def get_queryset(self):
        # Optionally, you can add filtering or sorting here
        return Category.objects.all().order_by('cat_name')

# Category Create View
class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'ad/category_form.html'  # Template for creating a category
    success_url = reverse_lazy('category_list')  # Redirect to the category list after creation
    success_message = "La catégorie a été créée avec succès."  # Success message

    def form_valid(self, form):
        # Optionally, you can add additional logic here before saving the form
        return super().form_valid(form)

# Category Update View
class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'ad/category_form.html'  # Template for updating a category
    success_url = reverse_lazy('category_list')  # Redirect to the category list after update
    success_message = "La catégorie a été mise à jour avec succès."  # Success message

    def form_valid(self, form):
        # Optionally, you can add additional logic here before saving the form
        return super().form_valid(form)

# Category Delete View
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'ad/delete.html'  # Template for confirming deletion
    success_url = reverse_lazy('category_list')  # Redirect to the category list after deletion

    def delete(self, request, *args, **kwargs):
        messages.success(request, "La catégorie a été supprimée avec succès.")  # Success message
        return super().delete(request, *args, **kwargs)