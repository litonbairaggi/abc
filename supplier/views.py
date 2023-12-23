from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier
from .forms import SupplierForm, SupplierDateSearchForm
from django.contrib import messages

# Create your views here.

def create(request):
    form = SupplierForm()
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier created successfully')
            return redirect('supplier_read')
    context = {
        'form': form
    }
    return render(request, 'supplier/create.html', context)


def supplier_read(request):
    form = SupplierDateSearchForm(request.POST or None)
    supplier_data = Supplier.objects.all().order_by('-id')
    context = {
        'supplier_data': supplier_data,
        'form':form,
    }
    if request.method == 'POST':
        supplier_data = Supplier.objects.filter(
										updated_at__range=[
																form['start_date'].value(),
																form['end_date'].value()
															]
										)
    context = {
        'supplier_data': supplier_data,
        'form':form,
    }
    return render(request, 'supplier/read.html', context)


def supplier_update(request, pk):
    get_supplier_data = get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(instance=get_supplier_data)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=get_supplier_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully')
            return redirect('supplier_read')
    context = {
        'form': form
    }
    return render(request, 'supplier/update.html', context)


def supplier_delete(request, pk):
    get_supplier = get_object_or_404(Supplier, pk=pk)
    get_supplier.delete()
    messages.error(request, 'Supplier delete successfully')
    return redirect('supplier_read')