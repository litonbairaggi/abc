from django.db import models
from django.db import models
from django.utils.timezone import now
from supplier.models import Supplier
from remarks.models import Remarks
from unit.models import Unit
from file.models import File
from stock.models import Stock
import datetime
from datetime import date
from django.utils import timezone

# Create your models here.

class WorkOrder(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=False, related_name='suppliersname')
    buyer_name = models.CharField(max_length=64, blank=False, null=True)
    po_no = models.CharField(max_length=32, null=True, blank=True)
    file_no = models.ForeignKey(File, on_delete=models.CASCADE, blank=False, related_name='file_nos')
    style_no = models.CharField(max_length=32, null=True, blank=True)
    work_order = models.CharField(max_length=64, null=True, blank=True, unique=True)
    work_order_date = models.DateField(auto_now_add=True, auto_now=False)
    master_lc_sc = models.CharField(max_length=64, null=True, blank=True)
    remarks = models.ForeignKey(Remarks, on_delete=models.CASCADE, blank=False, related_name='remarksname')
    
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return str(self.work_order)

    def get_items_list(self):
        return WorkOrderItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = WorkOrderItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total = total + item.totalprice
        return total

    def save(self, *args, **kwargs):
        if not self.work_order:
            # Generate a unique number based on date
            today = timezone.now()
            work_order_numbers = "{:04d}{:02d}{:02d}".format(today.year, today.month, today.day)
            work_order_number = work_order_numbers[2:]
            # Find the latest work order with the same date
            latest_work_order = WorkOrder.objects.filter(work_order__startswith=work_order_number).order_by('-work_order').first()
            if latest_work_order:
                # Extract the numeric part, increment it by 1, and append to the work_order_number
                latest_order_number = int(latest_work_order.work_order[len(work_order_number):])
                new_order_number = latest_order_number + 1
                self.work_order = f"{work_order_number}{new_order_number:04d}"
            else:
                # If no previous work orders for the current date, start with 0001
                self.work_order = f"{work_order_number}0001"
        super().save(*args, **kwargs)
        
#contains the purchase stocks made
class WorkOrderItem(models.Model):
    billno = models.ForeignKey(WorkOrder, on_delete = models.CASCADE, related_name='workorderbillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='workorderitem')
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    totalprice = models.DecimalField(max_digits=12, decimal_places=2)    
    uom = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=False, related_name='uom_workorders')
    size = models.CharField(max_length=64, blank=True, null=True)
    style = models.CharField(max_length=64, blank=True, null=True)
    color = models.CharField(max_length=64, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.billno.work_order)
    

#contains the other details in the purchases bill
class WorkOrderDetails(models.Model):
    billno = models.ForeignKey(WorkOrder, on_delete = models.CASCADE, related_name='workorders_billno')
    
    eway = models.CharField(max_length=50, blank=True, null=True)    
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "Id no: " + str(self.billno.billno)