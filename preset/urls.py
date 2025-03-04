from django.urls import path
from . import views

urlpatterns = [
# صفحة عملاء سرا الرئيسية +

path('packege' , views.packege , name='packege'),
path('packege_details/<str:id>' , views.packege_details , name='packege_details'),
# path('brands_dashbord/<str:id>' , views.brands_dashbord , name='brands_dashbord'), 
path('add_new_packages' , views.add_new_packages , name='add_new_packages'),  
# path('add_new_packages' , views.add_new_packages , name='add_new_packages'),  
path('section_details/<str:id>' , views.section_details , name='section_details'), 
path('add_termsPage/<str:id>' , views.add_termsPage , name='add_termsPage'),
path('add_new_terms' , views.add_new_terms , name='add_new_terms'),   
path('add_new_term_title/<str:id>' , views.add_new_term_title , name='add_new_term_title'), 
path('update_term_title/<str:id>' , views.update_term_title , name='update_term_title'),
path('delete_term/<str:id>' , views.delete_term , name='delete_term'), 

path('delete_package/<str:id>' , views.delete_package , name='delete_package'), 
path('edit_pck_title/<str:id>' , views.edit_pck_title , name='edit_pck_title'), 
path('deleteTitle/<str:id>' , views.deleteTitle , name='deleteTitle'), 
path('upload_packge_details/<str:id>' , views.upload_packge_details , name='upload_packge_details'),    
]