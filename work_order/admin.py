from django.contrib import admin
from .models import WorkOrder, WorkOrderItem, WorkOrderDetails
# Register your models here.

# admin.site.register(PurchaseBill)
# admin.site.register(WorkOrderItem)
admin.site.register(WorkOrderDetails)


@admin.register(WorkOrder)
class PurchaseBillAdmin(admin.ModelAdmin):
    list_display = ('billno', 'supplier', 'buyer_name', 'po_no', 'file_no', 'style_no', 'work_order', 'work_order_date', 'master_lc_sc', 'remarks', 'created_at')
    list_filter = ('supplier', 'remarks', 'created_at')
    search_fields = ('work_order', 'po_no', 'buyer_name')

@admin.register(WorkOrderItem)
class WorkOrderItemAdmin(admin.ModelAdmin):
    list_display = ('billno', 'stock', 'quantity', 'unit_price', 'totalprice', 'uom', 'size', 'style', 'color', 'created_at')
    list_filter = ('billno__supplier', 'stock', 'uom')
    search_fields = ('billno__work_order', 'stock__name', 'style', 'color')