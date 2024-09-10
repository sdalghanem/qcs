from django.contrib import admin
from .models import * 
# Register your models here.
class Term_titleAdmin(admin.ModelAdmin):
    list_display = ('section'  , 'packege_id' )   

class Preset_termsAdmin(admin.ModelAdmin):
    list_display = ('description'  , 'term_title_id' )     

admin.site.register(Packege)
admin.site.register(Term_title ,Term_titleAdmin)
admin.site.register(Preset_terms , Preset_termsAdmin)