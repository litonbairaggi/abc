from rest_framework import serializers
from .models import WorkOrder, WorkOrderItem

class WorkOrderSerializer(serializers.ModelSerializer):
    supplier = serializers.CharField(source='supplier.supplier_name')
    file_no = serializers.CharField(source='file_no.file')
    
    class Meta:
        model = WorkOrder
        # fields = ['style_no', 'file_no', 'master_lc_sc', 'buyer_name', 'supplier']
        fields = '__all__'
        

class WorkOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderItem
        # fields = ['quantity', 'size', 'style', 'color']
        fields = '__all__'