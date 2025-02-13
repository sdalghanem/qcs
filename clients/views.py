from django.shortcuts import redirect, render
from .models import *
from report.models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate , login as auth_login , logout
from . import dashboard_view , brands_view , departments_view
import datetime
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
            request.session['companyName'] = mngCompany.company_id.description
            print(mngCompany.position)
            # المنصب بناء على الارقام
            # اذا 0 يعني مدير عام شركة
            current_year = datetime.datetime.now().year

            if mngCompany.position == '0':
                request.session['position'] = mngCompany.position
                return redirect('gm_dashboard' , y = current_year , q='0') # يحول على الرابط اللي اسمه هوم 
          # مدير عام براند محدد
            elif mngCompany.position == '1' :
                brand = Brand.objects.get(gm_manager_id = mngCompany.id)
                request.session['position'] = mngCompany.position
                request.session['brandName'] = brand.description
                request.session['brand_id'] = brand.id
                request.session['brandLogo'] = str(brand.logo)
                return redirect('regions_rate' , id = brand.id , y = current_year, q = '0')
            # مدير  براند منطقة محددة
            elif mngCompany.position == '2' :
                brandRegion = Brand_regionManager.objects.get(manager_id = mngCompany.id)
                request.session['position'] = mngCompany.position
                request.session['brandName'] = brandRegion.Brand_id.description
                request.session['brand_id'] = brandRegion.Brand_id.id
                request.session['brandLogo'] = str(brandRegion.Brand_id.logo)
                request.session['regionName'] = brandRegion.region_id.name
                request.session['region_id'] = brandRegion.region_id.id
                return redirect('cities_rate',  id = brandRegion.region_id.id , brand_id = brandRegion.Brand_id.id , y = current_year,q = '0')
                                
            # مدير  براند مدينة محددة
            elif mngCompany.position == '3' :
                brand_city = Brand_cityManager.objects.get(manager_id = mngCompany.id)
                request.session['position'] = mngCompany.position
                request.session['brandName'] = brand_city.Brand_id.description
                request.session['brand_id'] = brand_city.Brand_id.id
                request.session['brandLogo'] = str(brand_city.Brand_id.logo)
                request.session['cityName'] = brand_city.city_id.name
                request.session['city_id'] = brand_city.city_id.id
                return redirect('districts_rate' , id = brand_city.city_id.id , brand_id =brand_city.Brand_id.id  , y = current_year,q = '0') 
            # مدير فرع محدد
            elif mngCompany.position == '4' : 
                branch = Branch.objects.get(manager_id = mngCompany.id)
                request.session['position'] = mngCompany.position
                request.session['brandName'] = branch.brand_id.description
                request.session['branchName'] = branch.description
                request.session['brandLogo'] = str(branch.brand_id.logo)
                request.session['branch_id'] = branch.id
                request.session['brand_id'] = branch.brand_id.id
                return redirect('reports_list' , id = branch.id , y = current_year,q = '0')  
            # مدير ادارة
            elif mngCompany.position == '5' :
                # id department - company name - company logo - mng name - mng postions
                dept = Department.objects.get(manager_id = mngCompany.id)
                request.session['position'] = mngCompany.position
                request.session['deptName'] = dept.description
                request.session['dept_id'] = dept.id
                return redirect('sections_rate' , id = dept.id ,y = current_year,q = '0')  
            # اذا مدير عام 0 يعني تدخل في تشييك البوزشن
            # اذا البزوشين 1 يعني مدير براند
            # يعني مدير براند منطقة 2
            # 3 يعني مدير براند مدينة
            # 4 يعني مدير فرع
            # 5 مدير ادارة
            # ابي اعرف شركته و منصبة
        else:
            return render(request , 'login.html' , {'back' : 'false'})
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
    branList = Brand.objects.filter(company_id = request.session['company_id'])
    data = {
    'companyLogo': request.session['companylogo'],
    'companyName': request.session['companyName'] ,
    'position': request.session['position'] ,
    'menubrands': branList ,
    'y' : '2024',
    'q' : 'q1',
    }
    return render(request , 'pages-contact-us.html' , data)

# Create your views here.
def pagefaq(request):
    branList = Brand.objects.filter(company_id = request.session['company_id'])
    data = {
    'companyLogo': request.session['companylogo'],
    'companyName': request.session['companyName'] ,
    'position': request.session['position'] ,
    'menubrands': branList ,
    'y' : '2024',
    'q' : 'q1',
    }
    return render(request , 'page-faq.html' , data) 

# def region_score(region_id , mngr_id):
#     brand = Brand.objects.get(gm_manager_id = mngr_id)
#     brandId = brand.id 

def logout_client(request):
    logout(request)
    return redirect('/clients/login')  # Redirect to login page after logging out