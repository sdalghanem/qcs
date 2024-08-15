from django.urls import path
from . import views
from . import officials
from . import api
from . import brands_view
from . import departments_view
from . import dashboard_view
urlpatterns = [
# صفحة عملاء سرا الرئيسية +
# path('' , views.index , name='home'),
path('login' , views.login_backend , name='login'),
path('forget_password' , views.forget_password , name='forget_password'), 
# لوحة التحكم  
path('gm_dashboard' , dashboard_view.gm_dashboard , name='gm_dashboard'), 
path('brandManager_dashboard' , dashboard_view.brandManager_dashboard , name='brandManager_dashboard'), 
path('brandRegionManager_dashboard' , dashboard_view.brandRegionManager_dashboard , name='brandRegionManager_dashboard'), 
path('brandCityManager_dashboard' , dashboard_view.brandCityManager_dashboard , name='brandCityManager_dashboard'), 
path('brach_Manager_dashboard' , dashboard_view.brach_Manager_dashboard , name='brach_Manager_dashboard'),  
path('dept_Manager_dashboard' , dashboard_view.dept_Manager_dashboard , name='dept_Manager_dashboard'),
#brands_view العلامات التجارية
path('regions_rate/<str:id>' , brands_view.regions_rate , name='regions_rate'),
path('cities_rate/<str:id>/<str:brand_id>' , brands_view.cities_rate , name='cities_rate'),
path('districts_rate/<str:id>/<str:brand_id>' , brands_view.districts_rate , name='districts_rate'),
path('branchs_rate/<str:id>/<str:brand_id>' , brands_view.branchs_rate , name='branchs_rate'),
path('reports_list/<str:id>' , brands_view.reports_list , name='reports_list'), 
path('show_report/<str:id>' , brands_view.show_report , name='show_report'),
# هذي الصفحة تحتاجها لتقييم الادارات
path('report' , views.report , name='report'),
#departments_view الادارات
path('departments_rate' , departments_view.departments_rate , name='departments_rate'),  
path('sections_rate/<str:id>' , departments_view.sections_rate , name='sections_rate'), 
path('terms_rate/<str:id>' , departments_view.terms_rate , name='terms_rate'),
# home
path('profile' , views.profile , name='profile'),
path('queries' , views.queries , name='queries'), 
path('contactus' , views.contactus , name='contactus'), 
path('pagefaq' , views.pagefaq , name='pagefaq'),
# المسؤولين
path('offhome' , officials.index , name='offhome'),
path('offqueries' , officials.queries , name='offqueries'), 
path('offreport_table' , officials.report_table , name='offreport_table'), 
path('offreport' , officials.report , name='offreport'),
#APIs
path('cities_list' , api.cities_list , name='cities_list' ),
path('district_list' , api.district_list , name='district_list' ), 
path('branch_list' , api.branch_list , name='branch_list' ),
path('sections_list' , api.sections_list , name='sections_list' ), 
path('reports_list' , api.reports_list , name='reports_list' ), 
path('view_report' , api.view_report , name='view_report' ), 
path('get_responisbles' , api.get_responisbles , name='get_responisbles' ),
path('get_percentage' , api.get_percentage , name='get_percentage' ),

]
