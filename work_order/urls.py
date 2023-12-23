from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from .views import WorkOrderDetailView

urlpatterns = [
    path('create/', views.WorkOrderCreateView.as_view(), name='create'),
    path('', views.wo_read, name='wo_read'),
    path('report/', views.woReport_read, name='wo_report'),
    path("bill/<billno>", views.WorkOrderView.as_view(), name="wo_bill"),
    path('delete/<int:pk>/', views.workorder_delete, name='wo_delete'), 
    # path('api/<int:pk>/', WorkOrderDetailView.as_view(), name='workorder_detail'),
    path('api/<str:work_order>/', WorkOrderDetailView.as_view(), name='workorder_detail'), 
    # path('api/item/<str:work_order>/', WorkOrderItemDetailView.as_view(), name='workorder_detail'),
]