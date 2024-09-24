from django.urls import path
from . import views

urlpatterns = [
# صفحة عملاء سرا الرئيسية +

path('show_orders' , views.show_orders , name='show_orders'),
path('add_newZone/<str:id>' , views.add_newZone , name='add_newZone'),
path('insert_responsible/<str:brandid>/<str:termid>' , views.insert_responsible , name='insert_responsible'),
path('show_responsible/<str:id>' , views.show_responsible , name='show_responsible'), 
path('delete_responsible/<str:id>' , views.delete_responsible , name='delete_responsible'),
] 