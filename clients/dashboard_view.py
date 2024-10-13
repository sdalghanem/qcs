from django.shortcuts import redirect, render
from .models import *
from report.models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate , login as auth_login , logout

##
# تخصص كل لوحة تحكم لكل منصب باقي

# صفحة دخول لوحة التحكم للمدير العام
def gm_dashboard(request):
    if request.user.is_authenticated:
        brands = Brand.objects.filter(company_id = request.session['company_id'])
        brandsList = []
        for b in brands:
            brandName = b.description
            brandid = b.id
            row = {
                'brandName' : brandName ,
                'brandid' : brandid,
                
            }
            brandsList.append(row)
        #print('تشغيييييل')
        print(request.session['companylogo'])
        data = {
            'menubrands' : brandsList,
            'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
            'mngPostion' : 'مدير عام' ,
           # 'companyName' : request.session['companyName'],
            'companyLogo': request.session['companylogo'],
            'brands' : brands,

        }
        return render(request , 'dashboards/dashboard.html' , data)
    else:
        return render(request , 'login.html')
    
def brandManager_dashboard(request ):
    data = {
        'mngName' : f" {request.session['firestName']}  {request.session['lastName']}" ,
        'mngPostion' :f" مدير  {request.session['brandName']}" ,
        'brand_id' : request.session['brand_id'],
        'brandName': request.session['brandName'],
        'brandLogo': request.session['brandLogo'],
    }
    return render(request , 'dashboards/brandManager_dashboard.html' , data)
    

def brandRegionManager_dashboard(request):
    data = {
        'mngName' : f" {request.session['firestName']}  {request.session['lastName']}" ,
        'mngPostion' :f" مدير  {request.session['brandName']} { request.session['regionName']}" ,
        'brand_id' : request.session['brand_id'],
        'brandName': request.session['brandName'],
        'brandLogo': request.session['brandLogo'],
        'regionName': request.session['regionName'] ,
        'region_id': request.session['region_id'] ,
            }
    return render(request , 'dashboards/brandRegionManager_dashboard.html' , data)

def brandCityManager_dashboard(request):
    data = {
            'mngName' : f" {request.session['firestName']}  {request.session['lastName']}" ,
            'mngPostion' :f" مدير  {request.session['brandName']} { request.session['cityName']}" ,
            'brand_id' : request.session['brand_id'],
            'brandName': request.session['brandName'],
            'brandLogo': request.session['brandLogo'],
            'cityName': request.session['cityName'] ,
            'city_id': request.session['city_id'] ,     
            }
    return render(request , 'dashboards/brandCityManager_dashboard.html' , data) 

def brach_Manager_dashboard(request):
    data = {
            'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
            'mngPostion' :'  مدير فرع ' + ' ' + request.session['branchName'] ,
            'brandName': request.session['brandName'],
            'brandLogo': request.session['brandLogo'],
            'branch_id' : request.session['branch_id'],
            'branchName' : request.session['branchName']
            }
    return render(request , 'dashboards/brach_Manager_dashboard.html' , data)


def dept_Manager_dashboard(request):
    # id department - company name - company logo - mng name - mng postions
    data = {
            'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
            'mngPostion' :'  مدير ادارة ' + ' ' + request.session['deptName'] ,
            'companyName': request.session['companyName'],
            'companylogo': request.session['companylogo'],
            'deptName': request.session['deptName'],
            'dept_id' : request.session['dept_id'],
            }
    print(data)
    return render(request , 'dashboards/dept_Manager_dashboard.html' , data)

