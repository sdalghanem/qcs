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

        }
        return render(request , 'dashboards/dashboard.html' , data)
    else:
        return render(request , 'login.html')
    
def brandManager_dashboard(request):
    data = {
        'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
        'mngPostion' :'مدير ' + ' ' + request.session['brandName']
    }
    return render(request , 'dashboards/brandManager_dashboard.html' , data)
    # if request.user.is_authenticated:
    #     brands = Brand.objects.filter(company_id = request.session['company_id'])
    #     brandsList = []
    #     for b in brands:
    #         brandName = b.description
    #         brandid = b.id
    #         row = {
    #             'brandName' : brandName ,
    #             'brandid' : brandid,
    #         }
    #         brandsList.append(row)
    #     #print('تشغيييييل')
    #     #print(brandsList)
    #     data = {
    #         'menubrands' : brandsList,
    #         'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
    #         'mngPostion' : 'مدير عام'
    #     }
    #     return render(request , 'dashboard.html' , data)
    # else:
    #     return render(request , 'login.html')

def brandRegionManager_dashboard(request):
    data = {
            'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
            'mngPostion' :'مدير ' + ' ' + request.session['brandName'] + ' ' + request.session['regionName']
            }
    return render(request , 'dashboards/brandRegionManager_dashboard.html' , data)

def brandCityManager_dashboard(request):
    data = {
            'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
            'mngPostion' :'  مدير مدينة ' + ' ' + request.session['brandName'] + ' ' + request.session['cityName']
           
            }
    return render(request , 'dashboards/brandCityManager_dashboard.html' , data) 

def brach_Manager_dashboard(request):
    data = {
            'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
            'mngPostion' :'  مدير فرع ' + ' ' + request.session['branchName'] 
            }
    return render(request , 'dashboards/brach_Manager_dashboard.html' , data)