from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def create(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully')
            return redirect('category_read')
    context= {
        'form': form
    }
    return render(request, 'category/create.html', context)


def category_read(request):
    category_data = Category.objects.all()
    context = {
        'category_data':category_data
    }
    return render(request, 'category/read.html', context)


def category_update(request, pk):
    get_category_data = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=get_category_data)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=get_category_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('category_read')
    context = {
        'form': form
    }    
    return render(request, 'category/update.html', context)


def category_delete(request, pk):
    get_category = get_object_or_404(Category, pk=pk)
    get_category.delete()
    messages.error(request, 'Category deleted successfully')
    return redirect('category_read')