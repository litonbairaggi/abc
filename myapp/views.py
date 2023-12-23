from django.shortcuts import render, get_object_or_404, redirect
from .models import Myapp
from .forms import MyappForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# Create
def create(request):
    form = MyappForm()
    if request.method == 'POST':
        form = MyappForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Myapp created successfully')
            return redirect('myapp_read')
    context= {
        'form': form
    }
    return render(request, 'myapp/create.html', context)


def myapp_read(request):
    myapp_data = Myapp.objects.all()
    context = {
        'myapp_data':myapp_data
    }
    return render(request, 'myapp/read.html', context)
