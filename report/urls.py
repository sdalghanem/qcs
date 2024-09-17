from django.urls import path
from . import views

urlpatterns = [
# صفحة عملاء سرا الرئيسية +
path('add_term/<str:id>' , views.add_term , name='add_term'),

]