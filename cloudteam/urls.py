from django.urls import path
from . import views

urlpatterns = [
# صفحة عملاء سرا الرئيسية +
path('company_list' , views.company_list , name='company_list'), 
path('add_new_company' , views.add_new_company , name='add_new_company'),
path('brands_dashbord/<str:id>' , views.brands_dashbord , name='brands_dashbord'), 
path('add_new_brand/<str:id>' , views.add_new_brand , name='add_new_brand'), 
path('add_new_branch/<str:id>' , views.add_new_branch , name='add_new_branch'),
path('users_managment/<str:id>' , views.users_managment , name='users_managment'), 
path('departments/<str:id>' , views.departments , name='departments'), 


path('update_company_mngs/<str:id>' , views.update_company_mngs , name='update_company_mngs'), 
path('update_branch_mngs/<str:id>' , views.update_branch_mngs , name='update_branch_mngs'), 
path('update_position_mngs/<str:id>' , views.update_position_mngs , name='update_position_mngs'), 

path('add_new_dept/<str:id>' , views.add_new_dept , name='add_new_dept'),  
path('add_new_sec/<str:id>' , views.add_new_sec , name='add_new_sec'),
path('edit_departmentInfo/<str:id>' , views.edit_departmentInfo , name='edit_departmentInfo'),  

path('edit_secInfo/<str:id>' , views.edit_secInfo , name='edit_secInfo'),  
path('brand_terms/<str:id>' , views.brand_terms , name='brand_terms'),  
path('save_packege/' , views.save_packege , name='save_packege'),  

]
