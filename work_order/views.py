from django.shortcuts import render, redirect, get_object_or_404
from stock.models import Stock
from django.contrib import messages
from .models import WorkOrder, WorkOrderItem, WorkOrderDetails
from .forms import WorkOrderDetailsForm, WorkOrderItemFormset, WorkOrderForm, WorkOrderSearchForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    View, 
    ListView,
    DeleteView
)
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
from django.utils.decorators import method_decorator
from django.forms.models import modelformset_factory

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import WorkOrderSerializer, WorkOrderItemSerializer
from .forms import UserUpdateForm
# Create your views here.

# used to generate a id object and save items

@method_decorator(login_required, name='dispatch')
class WorkOrderCreateView(View):                                                 
    template_name = 'workorder/create.html'
    
    def get(self, request):
        form = WorkOrderForm(request.GET or None)
        formset = WorkOrderItemFormset(request.GET or None)                       # renders an empty formset
        stocks = Stock.objects.filter(is_deleted=False)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
        else:
            u_form = UserUpdateForm(instance=request.user)
        context = {
            'form'      : form,
            'formset'   : formset,
            'stocks'    : stocks, 
            'u_form'    : u_form,
        }                                                                        # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request):
        form = WorkOrderForm(request.POST)
        formset = WorkOrderItemFormset(request.POST) 
        # recieves a post method for the formset
        
        if form.is_valid() and formset.is_valid():
            # saves workorder
            billobj = form.save(commit=False)
            billobj.save() 
            
            for form in formset:                                                   # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj               

                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)         # gets the item
                # calculates the total price
                billitem.totalprice = billitem.unit_price * billitem.quantity
                
                # updates quantity in stock db
                # stock.quantity += billitem.quantity                               # updates quantity
                
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success(request, "Work Order items have been create successfully")
            return redirect('wo_read')
        form = WorkOrderForm(request.GET or None)
        formset = WorkOrderItemFormset(request.GET or None)
        context = {
            'form'      : form,
            'formset'   : formset,            
        }
        return render(request, self.template_name, context)    
    

# Read
@login_required
@allowed_users(allowed_roles=['admin', 'merchandiser', 'store'])
def wo_read(request):
    form = WorkOrderSearchForm(request.POST or None)
    bills = WorkOrder.objects.all().order_by('-time')
    # abc = Stock.objects.all().order_by('id')
    stock_datas = Stock.objects.all().order_by('-time')
    context = {
        'bills':bills,
        'form':form,
        'stock_datas':stock_datas,
    }
    if request.method == 'POST':
        bills = WorkOrder.objects.filter(
										updated_at__range=[
																form['start_date'].value(),
																form['end_date'].value()
															]
										)
    context = {
        'bills':bills,
        'form':form,
        'stock_datas':stock_datas,
    }
    return render(request, 'workorder/read.html', context)


# Work Order Report Read
@login_required
@allowed_users(allowed_roles=['admin', 'merchandiser', 'store'])
def woReport_read(request):
    form = WorkOrderSearchForm(request.POST or None)
    bills = WorkOrder.objects.all().order_by('-time')
    context = {
        'bills':bills,
        'form':form,
    }
    if request.method == 'POST':
        bills = WorkOrder.objects.filter(
										updated_at__range=[
																form['start_date'].value(),
																form['end_date'].value()
															]
										)
    context = {
        'bills':bills,
        'form':form,
    }
    return render(request, 'workorder/report.html', context)

# used to display the workorder bill object
@method_decorator(login_required, name='dispatch')
class WorkOrderView(View):
    model = WorkOrder
    template_name = "bill/wo_bill.html"

    def get(self, request, billno):
        context = {
            'bill'          : WorkOrder.objects.get(billno=billno),
            'items'         : WorkOrderItem.objects.filter(billno=billno),
            # 'billdetails'   : WorkOrderDetails.objects.get(billno=billno),
            # 'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = WorkOrderDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = WorkOrderDetails.objects.get(billno=billno)
            
            billdetailsobj.eway = request.POST.get("eway")    
            billdetailsobj.veh = request.POST.get("veh")
            billdetailsobj.destination = request.POST.get("destination")
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.cgst = request.POST.get("cgst")
            billdetailsobj.sgst = request.POST.get("sgst")
            billdetailsobj.igst = request.POST.get("igst")
            billdetailsobj.cess = request.POST.get("cess")
            billdetailsobj.tcs = request.POST.get("tcs")
            billdetailsobj.total = request.POST.get("total")
            
            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill'          : WorkOrder.objects.get(billno=billno),
            'items'         : WorkOrderItem.objects.filter(billno=billno),
            'billdetails'   : WorkOrderDetails.objects.get(billno=billno),
            # 'wo_base'     : self.wo_base,
        }
        return render(request, self.template_name, context)    


# Delete
@login_required
@allowed_users(allowed_roles=['admin'])
def workorder_delete(request, pk):
    get_workorder = get_object_or_404(WorkOrder, pk=pk)
    # Retrieve items associated with the workorder
    items = WorkOrderItem.objects.filter(billno=get_workorder.billno)
    for item in items:
        stock = get_object_or_404(Stock, name=item.stock.name)
        if not stock.is_deleted:
            stock.save()
    get_workorder.delete()
    messages.success(request, 'Work Order has been deleted successfully')
    return redirect('wo_read')


# @method_decorator(login_required, name='dispatch')
class WorkOrderDetailView(APIView):
    def get(self, request, work_order):
        try:
            workorder = WorkOrder.objects.get(work_order=work_order)
            workorder_serializer = WorkOrderSerializer(workorder)
            workorder_items = WorkOrderItem.objects.filter(billno=workorder)
            workorder_items_serializer = WorkOrderItemSerializer(workorder_items, many=True)
            response_data = {
                'workorder': workorder_serializer.data,
                'workorder_items': workorder_items_serializer.data,
            }
            return Response(response_data)
        except Exception as e:
            return Response(str(e), status=404)