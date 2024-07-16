from django.shortcuts import redirect, render
from .models import *
from report.models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate , login as auth_login , logout
from . import dashboard_view

# صفحة دخول لوحة التحكم للمدير العام
# def index(request):
#     if request.user.is_authenticated:
#         brands = Brand.objects.filter(company_id = request.session['company_id'])
#         brandsList = []
#         for b in brands:
#             brandName = b.description
#             brandid = b.id
#             row = {
#                 'brandName' : brandName ,
#                 'brandid' : brandid,
#             }
#             brandsList.append(row)
#         #print('تشغيييييل')
#         #print(brandsList)
#         data = {
#             'menubrands' : brandsList,
#             'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
#             'mngPostion' : request.session['position']
#         }
#         return render(request , 'dashboard.html' , data)
#     else:
#         return render(request , 'login.html')

# Create your views here.
# تسجيل دخول لمدير عام الشركة
## يقدر يشوف تقييم الادارات
## تقييم الفروع كلها

# مدير براند
# ## يشوف البراند حقه بدون الادارات
# مدير منطقة
# ## يشوف تقييم جميع الفروع بالمنطقة الخاصه فيه فقط
# مدير مدينه 
## يشوف تقييم الفروع الخاصه في مدينته فقط
# مدير فرع 
## يشوف التقيم الخاص بفرعه فقط
# مدير ادارة
# مدير قسم


def login_backend(request):
    if request.method =='POST':
        mngUsername = request.POST['username']
        mngPassword = request.POST['password']
        result = authenticate(username = mngUsername , password = mngPassword)
        print(result)
        if result is not None:
            auth_login(request, result) 
            userInfo = User.objects.get(username = mngUsername)
            # save data on session
            request.session['id'] = userInfo.id
            request.session['firestName'] = userInfo.first_name
            request.session['lastName'] = userInfo.last_name   
            request.session['username'] = userInfo.username
            mngCompany = Managers.objects.get(user = userInfo)
            request.session['company_id'] = mngCompany.company_id.id
            request.session['companylogo'] = str(mngCompany.company_id.logo)
            #request.session['companyName'] = mngCompany.company_id.description
            print(mngCompany.position)
            # المنصب بناء على الارقام
            # اذا المدير العام 1 يعني مدير عام شركة
            if mngCompany.gm_manager == 1 :
                return redirect('gm_dashboard') # يحول على الرابط اللي اسمه هوم 
          
            elif mngCompany.position == '1' :
                brand = Brand.objects.get(gm_manager_id = mngCompany.id)
                request.session['brandName'] = brand.description
                return redirect('brandManager_dashboard')
            elif mngCompany.position == '2' :
                brandRegion = Brand_regionManager.objects.get(manager_id = mngCompany.id)
                request.session['brandName'] = brandRegion.Brand_id.description
                request.session['regionName'] = brandRegion.region_id.name
                return redirect('brandRegionManager_dashboard')
            elif mngCompany.position == '3' :
                brand_city = Brand_cityManager.objects.get(manager_id = mngCompany.id)
                request.session['brandName'] = brand_city.Brand_id.description
                request.session['cityName'] = brand_city.city_id.name
                return redirect('brandCityManager_dashboard') 
            elif mngCompany.position == '4' : 
                branch = Branch.objects.get(manager_id = mngCompany.id)
                request.session['brandName'] = branch.brand_id.description
                request.session['branchName'] = branch.description
                return redirect('brach_Manager_dashboard') 
            # اذا مدير عام 0 يعني تدخل في تشييك البوزشن
            # اذا البزوشين 1 يعني مدير براند
            # يعني مدير براند منطقة 2
            # 3 يعني مدير براند مدينة
            # 4 يعني مدير فرع

            # ابي اعرف شركته و منصبة
            
        else:
            return render(request , 'login.html')
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
def contactus(request):
    return render(request , 'pages-contact-us.html')

# Create your views here.
def pagefaq(request):
    return render(request , 'page-faq.html') 

# def region_score(region_id , mngr_id):
#     brand = Brand.objects.get(gm_manager_id = mngr_id)
#     brandId = brand.id 
