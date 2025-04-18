from django.shortcuts import render, redirect
from user.models import Product, Category  # Remplacé Ad par Product
from user.forms import ProductForm, CategoryForm  # Ajusté AdForm à ProductForm
from django.contrib.auth.decorators import login_required
from .decorators import admin_required  # Si vous placez le décorateur dans un fichier séparé

@login_required
@admin_required
def home(request):
    products = Product.objects.all()
    return render(request, 'ad/home.html', {'products': products})

@login_required
@admin_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('ad-home')
    return render(request, 'ad/delete.html', {'product': product})

@login_required
@admin_required
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('ad-home')
    return render(request, 'ad/update.html', {'form': form})

@login_required
@admin_required
def create_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Note : ajusté à category_list
    return render(request, 'ad/category/create.html', {'form': form})

@login_required
@admin_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'ad/category/list.html', {'categories': categories})

@login_required
@admin_required
def update_category(request, category_id):
    category = Category.objects.get(id=category_id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    return render(request, 'ad/category/update.html', {'form': form})