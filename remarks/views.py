from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Remarks
from .forms import RemarksForm, RemarksDateSearchForm

# Create your views here.


def create(request):
    form = RemarksForm()
    if request.method == 'POST':
        form = RemarksForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Remarks created successfully')
            return redirect('remarks_read')
    context= {
        'form': form
    }
    return render(request, 'remarks/create.html', context)

def remarks_read(request):
    form = RemarksDateSearchForm(request.POST or None)
    remarks_data = Remarks.objects.all().order_by('-id')
    context = {
        'remarks_data':remarks_data,
        'form':form,
    }
    if request.method == 'POST':
        remarks_data = Remarks.objects.filter(
										updated_at__range=[
																form['start_date'].value(),
																form['end_date'].value()
															]
										)
    context = {
        'remarks_data':remarks_data,
        'form':form,
    }
    return render(request, 'remarks/read.html', context)


def remarks_update(request, pk):
    get_remarks_data = get_object_or_404(Remarks, pk=pk)
    form = RemarksForm(instance=get_remarks_data)
    if request.method == "POST":
        form = RemarksForm(request.POST, instance=get_remarks_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Remarks updated successfully')
            return redirect('remarks_read')
    context = {
        'form':form
    }
    return render(request, 'remarks/update.html', context)


def remarks_delete(reqest, pk):
    get_remarks = get_object_or_404(Remarks, pk=pk)
    get_remarks.delete()
    messages.error(reqest, 'Remarks deleted successfully')
    return redirect('remarks_read')