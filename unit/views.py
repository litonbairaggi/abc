from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Unit
from .forms import UnitForm, UnitDateSearchForm
# Create your views here.


def create(request):
    form = UnitForm()
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unit created successfully')
            return redirect('unit_read')
    context= {
        'form': form
    }
    return render(request, 'unit/create.html', context)


def unit_read(request):
    form = UnitDateSearchForm(request.POST or None)
    unit_data = Unit.objects.all().order_by('-id')
    context = {
        'unit_data':unit_data,
        'form':form,
    }
    if request.method == 'POST':
        unit_data = Unit.objects.filter(
										updated_at__range=[
																form['start_date'].value(),
																form['end_date'].value()
															]
										)
    context = {
        'unit_data':unit_data,
        'form':form,
    }
    return render(request, 'unit/read.html', context)


def unit_update(request, pk):
    get_unit_data = get_object_or_404(Unit, pk=pk)
    form = UnitForm(instance=get_unit_data)
    if request.method == "POST":
        form = UnitForm(request.POST, instance=get_unit_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unit updated successfully')
            return redirect('unit_read')
    context = {
        'form':form
    }
    return render(request, 'unit/update.html', context)

def unit_delete(reqest, pk):
    get_unit = get_object_or_404(Unit, pk=pk)
    get_unit.delete()
    messages.error(reqest, 'Unit deleted successfully')
    return redirect('unit_read')