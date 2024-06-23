from django.urls import path
from . import views

urlpatterns = [
# صفحة عملاء سرا الرئيسية +
path('company_list' , views.company_list , name='company_list'),


]
