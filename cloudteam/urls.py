from django.urls import path
from . import views , company_view , inspector_view , countries_views

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
path('regions_city_managers/<str:id>' , company_view.regions_city_managers , name='regions_city_managers'),
path('deleteRegionMngr/<str:id>' , company_view.deleteRegionMngr , name='deleteRegionMngr'), 
path('cities_managers/<str:regionID>/<str:brandID>' , company_view.cities_managers , name='cities_managers'), 
path('deletecityMngr/<str:id>/<str:regionID>' , company_view.deletecityMngr , name='deletecityMngr'), 
###############################################################
##### العنواين
##############################################################

path('show_region/' , countries_views.show_region , name='show_region'),  
path('delete_region/<str:id>' , countries_views.delete_region , name='delete_region'),  
path('show_city/<str:id>' , countries_views.show_city , name='show_city'),  
path('add_city/' , countries_views.add_city , name='add_city'),  
path('delete_city/<str:id>' , countries_views.delete_city , name='delete_city'),  
#path('show_district/<str:id>' , countries_views.show_district , name='show_district'),  
path('add_district/' , countries_views.add_district , name='add_district'),  
path('delete_district/<str:id>' , countries_views.delete_district , name='delete_district'),  


################################################################
path('save_packege/' , views.save_packege , name='save_packege'),   
path('remove_note/' , views.remove_note , name='remove_note'),
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
 path('get_evaluation_points/<int:zone_id>/<int:orID>', inspector_view.get_evaluation_points, name='get_evaluation_points'), 
 path('save_evaluation/<str:id>' , inspector_view.save_evaluation , name='save_evaluation'),   

] 
