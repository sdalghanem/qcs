from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import * 


# class MyAdminSite(AdminSite):
#     site_header = 'Custom Admin'
#     site_title = 'Custom Admin'
#     index_title = 'Dashboard'

# custom_admin_site = MyAdminSite(name='myadmin')
# custom_admin_site.register(Country)

admin.site.site_header = "QCS"
admin.site.site_title = "QCS"
admin.site.index_title = "نظام إدارة الجودة"

# الدول و المناطق و المدن و الأحياء
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name'  , 'country_id' )


class CityAdmin(admin.ModelAdmin):
    list_display = ('name'  , 'region_id' )     
    list_filter=( 'region_id', ) 
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name'  , 'city_id' )     
         

# الإدارات و الأقسام
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('description'  , 'company_id' , 'manager_id')     
    list_filter=('company_id__description' ,'manager_id')
    search_fields=('description',)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('description'  , 'department_id' , 'company_name' , 'manager_id') 
    list_filter=( 'department_id', 'manager_id')
    search_fields=('description',)    
     # استرجاع اسم المدينة
    def company_name(self , instance):
        return instance.department_id.company_id 
    company_name.short_description = 'الشركة'
# العلامات التجارية و الفروع
class BrandAdmin(admin.ModelAdmin):
    list_display = ('description'  , 'company_id'  , 'registerDate' ,'gm_manager_id')     
    list_filter=( 'company_id', 'gm_manager_id')
    search_fields=('description',)  
class BranchAdmin(admin.ModelAdmin):
    list_display = ('description'  , 'brand_id' ,'manager_id', 'district_id' ,'city','region', 'registerDate' )
    list_filter=( 'brand_id',)
    search_fields=('description',)  

    # استرجاع اسم المدينة
    def city(self , instance):
        return instance.district_id.city_id 
    city.short_description = 'المدينة'
 
     # استرجاع اسم المنطقة
    def region(self , instance):
        return instance.district_id.city_id.region_id 
    region.short_description = 'المنطقة'

class Brand_regionManagerAdmin(admin.ModelAdmin):
    list_display = ('manager_id'  , 'Brand_id' ,'region_id' ,'registerDate' )
    list_filter=( 'Brand_id', 'region_id' )
    search_fields=('manager_id','Brand_id')  

class Brand_cityManagerAdmin(admin.ModelAdmin):
    list_display = ('manager_id'  , 'Brand_id' , 'city_id' ,'registerDate')
    list_filter=( 'Brand_id', 'city_id' )
    search_fields=('manager_id','Brand_id')  

# class managerAdmin(admin.ModelAdmin):
#     list_display = ('manager_id'  , 'company_id' )


admin.site.register(Country)
admin.site.register(Region , RegionAdmin )
admin.site.register(City , CityAdmin )
admin.site.register(District , DistrictAdmin )

admin.site.register(Company)

admin.site.register(Department , DepartmentAdmin )
admin.site.register(Section , SectionAdmin )


admin.site.register(Brand , BrandAdmin )
admin.site.register(Branch , BranchAdmin )

# المدراء
admin.site.register(Managers )
admin.site.register(Brand_regionManager , Brand_regionManagerAdmin)
admin.site.register(Brand_cityManager , Brand_cityManagerAdmin )

