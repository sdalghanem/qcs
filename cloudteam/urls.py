from django.urls import path
from . import views

urlpatterns = [
# صفحة عملاء سرا الرئيسية +
path('company_list' , views.company_list , name='company_list'), 
path('add_new_company' , views.add_new_company , name='add_new_company'),
path('add_new_brand/<str:id>' , views.add_new_brand , name='add_new_brand'), 
path('add_new_branch/<str:id>' , views.add_new_branch , name='add_new_branch'),
path('users_managment/<str:id>' , views.users_managment , name='users_managment'),
]
