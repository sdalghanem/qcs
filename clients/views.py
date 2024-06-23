from django.shortcuts import render
from .models import *
from report.models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json

def index(request):
    brands = Brand.objects.filter(company_id = 1)
    brandsList = []
    for b in brands:
        brandName = b.description
        brandid = b.id
        row = {
            'brandName' : brandName ,
            'brandid' : brandid,
        }
        brandsList.append(row)
    print('تشغيييييل')
    print(brandsList)
    data = {
        'brands' : brandsList,
    }
    return render(request , 'dashboard.html' , data)

# Create your views here.
def login_backend(request):
    return render(request , 'login.html')

# Create your views here.
def forget_password(request):
    return render(request , 'forget_password.html')


# Create your views here.
# هذي الصفحة تحتاجها لتقييم الادارات
def report(request):
    return render(request , 'report.html')

# Create your views here.
def profile(request):
    return render(request , 'profile.html')

# الاستعلامات عن تقييمات الفروع.
def queries(request):
    countries = Country.objects.all()
    regions = Region.objects.filter(country_id = 1 )
    brands = Brand.objects.filter(company_id = 1)
    data = {
            'countries' : countries ,
            'regions' : regions ,
            'brands' : brands,
          }
    return render(request , 'queries.html' , data)

# Create your views here.
def officials_queries(request):
    managers = Managers.objects.filter(company_id = 1)
    departments = Department.objects.filter(company_id = 1)
    data = {
        'managers' : managers,
                    'departments' : departments,

        }
    return render(request , 'officials_queries.html' , data) 

# Create your views here.
def contactus(request):
    return render(request , 'pages-contact-us.html')

# Create your views here.
def pagefaq(request):
    return render(request , 'page-faq.html') 

# def region_score(region_id , mngr_id):
#     brand = Brand.objects.get(gm_manager_id = mngr_id)
#     brandId = brand.id 
