from django.urls import path
from . import views

urlpatterns = [
# صفحة عملاء سرا الرئيسية +

path('show_orders/<str:id>' , views.show_orders , name='show_orders'),
path('add_newZone/<str:id>' , views.add_newZone , name='add_newZone'),
path('insert_responsible/<str:brandid>/<str:termid>' , views.insert_responsible , name='insert_responsible'),
path('insert_note/<str:brandid>/<str:termid>' , views.insert_note , name='insert_note'),


path('show_responsible/<str:id>' , views.show_responsible , name='show_responsible'), 
path('delete_responsible/<str:id>' , views.delete_responsible , name='delete_responsible'),
path('new_order/<str:id>' , views.new_order , name='new_order'),
path('get_brand' , views.get_brand , name='get_brand'),
path('get_branch' , views.get_branch , name='get_branch'),
path('show_order_details/<str:id>' , views.show_order_details , name='show_order_details'),
path('submit_result/<str:resault>/<str:orderid>' , views.submit_result , name='submit_result'),
path('add_responsibles' , views.add_responsibles , name='add_responsibles'), 
path('term_cancel' , views.term_cancel , name='term_cancel'), 
path('add_brands_orders/<str:id>' , views.add_brands_orders , name='add_brands_orders'),  
path('process_responsible/<str:id>' , views.process_responsible , name='process_responsible'),
path('remove_order' , views.remove_order , name='remove_order'),


] 