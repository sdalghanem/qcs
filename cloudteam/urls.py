from django.urls import path
from . import views , company_view , inspector_view

urlpatterns = [
# بروفايل الشركة
path('company_list' , company_view.company_list , name='company_list'), 
path('add_new_company' , company_view.add_new_company , name='add_new_company'),
path('brands_dashbord/<str:id>' , company_view.brands_dashbord , name='brands_dashbord'), 
path('add_new_brand/<str:id>' , company_view.add_new_brand , name='add_new_brand'), 

path('add_new_branch/<str:id>' , company_view.add_new_branch , name='add_new_branch'),
path('users_managment/<str:id>' , company_view.users_managment , name='users_managment'), 
path('departments/<str:id>' , company_view.departments , name='departments'), 

path('update_company_mngs/<str:id>' , company_view.update_company_mngs , name='update_company_mngs'), 
path('update_branch_mngs/<str:id>' , company_view.update_branch_mngs , name='update_branch_mngs'), 
path('update_position_mngs/<str:id>' , company_view.update_position_mngs , name='update_position_mngs'), 

path('add_new_dept/<str:id>' , company_view.add_new_dept , name='add_new_dept'),  
path('add_new_sec/<str:id>' , company_view.add_new_sec , name='add_new_sec'),
path('edit_departmentInfo/<str:id>' , company_view.edit_departmentInfo , name='edit_departmentInfo'),  

path('edit_secInfo/<str:id>' , company_view.edit_secInfo , name='edit_secInfo'),  
path('brand_terms/<str:id>' , company_view.brand_terms , name='brand_terms'), 

##############################################################
path('save_packege/' , views.save_packege , name='save_packege'),  

# cloud team pages .
path('login_admin' , views.login_admin , name='login_admin'), 
path('logout_view' , views.logout_view , name='logout_view'), 

path('show_inspectors' , views.show_inspectors , name='show_inspectors'), 
path('new_inspectors_form' , views.new_inspectors_form , name='new_inspectors_form'),
path('edit_Inspectors/<str:id>' , views.edit_Inspectors , name='edit_Inspectors'), 
#####################################################################
############## الموظفين ##########################################
##################################################################
path('login_insp' , inspector_view.login_insp , name='login_insp'), 
path('emp_orders' , inspector_view.emp_orders , name='emp_orders'),  
path('evaluate/<str:id>' , inspector_view.evaluate , name='evaluate'),
] 
