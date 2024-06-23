from django.contrib import admin
from .models import * 

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user'  , 'mobile' , 'supervisor' ,'manager' , 'profile_img' )     

class cloudteam_DepartmentAdmin(admin.ModelAdmin):
    list_display = ('manager_id'  , 'description' )     

class cloudteam_SectionAdmin(admin.ModelAdmin):
    list_display = ('manager_id'  , 'description' ,'department_id' )  


admin.site.register(Employee , EmployeeAdmin)
admin.site.register(cloudteam_Department , cloudteam_DepartmentAdmin)
admin.site.register(cloudteam_Section , cloudteam_SectionAdmin)

