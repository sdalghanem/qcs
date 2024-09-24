from django.contrib import admin
from .models import *


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name'  , 'brand_id' )
    list_filter=('brand_id__description' ,)

class TermAdmin(admin.ModelAdmin):
    list_display = ('description'  , 'brand_id' , 'cancel' )
    list_filter=('brand_id__description' ,)

class Term_responsibleAdmin(admin.ModelAdmin):
    list_display = ('term_id'  , 'section_id' , 'zone_id' )
    list_filter=('zone_id__brand_id__description' , 'section_id__description')

class Term_scoreAdmin(admin.ModelAdmin):
    list_display = ('report_order_id'  , 'term_id' , 'score' , 'note' , 'registerDate')
    list_filter=('report_order_id__bransh_id__description' , )

class Score_historyAdmin(admin.ModelAdmin):
    list_display = ('report_order_id'  , 'total_score' , 'registerDate')
    list_filter=('report_order_id__bransh_id__description' , )

class Report_orderAdmin(admin.ModelAdmin):
    list_display = ('bransh_id'  , 'employee_id' , 'registerDate')
   

# Register your models here.
admin.site.register(Zone , ZoneAdmin)
admin.site.register(Term , TermAdmin)
admin.site.register(Term_responsible , Term_responsibleAdmin)
admin.site.register(Report_order , Report_orderAdmin)
admin.site.register(Term_score , Term_scoreAdmin)
admin.site.register(Score_history , Score_historyAdmin)
