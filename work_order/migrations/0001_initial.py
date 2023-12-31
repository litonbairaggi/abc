# Generated by Django 4.2.6 on 2023-12-11 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
        ('remarks', '0001_initial'),
        ('supplier', '0002_alter_supplier_date'),
        ('unit', '0001_initial'),
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('buyer_name', models.CharField(max_length=64, null=True)),
                ('po_no', models.CharField(blank=True, max_length=32, null=True)),
                ('style_no', models.CharField(blank=True, max_length=32, null=True)),
                ('work_order', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('work_order_date', models.DateField(auto_now_add=True)),
                ('master_lc_sc', models.CharField(blank=True, max_length=64, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_nos', to='file.file')),
                ('remarks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remarksname', to='remarks.remarks')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suppliersname', to='supplier.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('totalprice', models.DecimalField(decimal_places=2, max_digits=12)),
                ('size', models.CharField(blank=True, max_length=64, null=True)),
                ('style', models.CharField(blank=True, max_length=64, null=True)),
                ('color', models.CharField(blank=True, max_length=64, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workorderbillno', to='work_order.workorder')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workorderitem', to='stock.stock')),
                ('uom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uom_workorders', to='unit.unit')),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eway', models.CharField(blank=True, max_length=50, null=True)),
                ('veh', models.CharField(blank=True, max_length=50, null=True)),
                ('destination', models.CharField(blank=True, max_length=50, null=True)),
                ('po', models.CharField(blank=True, max_length=50, null=True)),
                ('cgst', models.CharField(blank=True, max_length=50, null=True)),
                ('sgst', models.CharField(blank=True, max_length=50, null=True)),
                ('igst', models.CharField(blank=True, max_length=50, null=True)),
                ('cess', models.CharField(blank=True, max_length=50, null=True)),
                ('tcs', models.CharField(blank=True, max_length=50, null=True)),
                ('total', models.CharField(blank=True, max_length=50, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workorders_billno', to='work_order.workorder')),
            ],
        ),
    ]
