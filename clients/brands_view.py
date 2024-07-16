from django.shortcuts import render
from .models import *
from report.models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json

# Create your views here.
def regions_rate(request , id):
    regioninfo =[]
    perlist=[]
    regionlist =[]
    mngs = Brand_regionManager.objects.filter(Brand_id = id )
    #final_score = Score_history.objects.filter(report_order_id=specific_id_value).latest('registerDate')
    brandName = ''
    brandLogo = ''
    for mng in mngs: 
        # اسم البرانج و اللوجو استخراج
        brandName = mng.Brand_id.description
        brandLogo = str(mng.Brand_id.logo)
        print(brandLogo)
        print(brandName)
        ############################################
        final_score = branchs_resault(mng.region_id , mng.Brand_id)
        total = 0
        score_list = []
        for fs in final_score:
            score_list.append(int(fs['score'])) 
        for sl in score_list:
            total += sl
        #print(len(score_list))
        if len(score_list) == 0 :
            percentage = 0
        else :
             percentage = int((total / len(score_list)) )
        #############################################
        #number +=1
        row = {
            'name' : mng.manager_id.user.first_name + ' ' + mng.manager_id.user.last_name,
            'region' : mng.region_id.name,
            'rate': percentage,
            'id' : mng.region_id.id , # id  المنطقة
            'brand_id' : mng.Brand_id.id
        }
        perlist.append(percentage)
        regionlist.append(mng.region_id.name )
        regioninfo.append(row)

    sorted_data = sorted(regioninfo, key=lambda x: x['rate'], reverse=True)
   
    data = {
        'row': sorted_data,
        'perlist':perlist ,
        'regionlist':json.dumps(regionlist) ,
        'brandName' :brandName ,
        'brandLogo' :brandLogo ,
    }
   
    print(regionlist)
    return render(request , 'brands/regionsRate.html' , data)


# فنكشن لتقييم المدن
def cities_rate(request , id ,brand_id):
    #id = region id
    # اول شي تجيب المدن اللي بوسط المنطقة
    cities = City.objects.filter(region_id = id)
    cityInfo = []
    # chart data
    perlist=[]
    citieslist=[]
    for c in cities:
        # ثاني شي تجيب اسامي المدراء
        if Brand_cityManager.objects.filter(Brand_id = brand_id , city_id = c.id).exists():
            mngs = Brand_cityManager.objects.filter(Brand_id = brand_id , city_id = c.id) #  اصلاح رقم اي دي العلامه التجارية
            for m in mngs:
                final_score = branchs_city_resault(m.city_id.id , m.Brand_id.id)
                total = 0
                score_list = []
                for fs in final_score:
                    score_list.append(int(fs['score'])) 
                for sl in score_list:
                    total += sl
                #print(len(score_list))
                if len(score_list) == 0 :
                    percentage = 0
                else :
                    percentage = int((total / len(score_list)) )
                
                cityRow = {
                            'cityName' : m.city_id.name , 
                            'mngName':m.manager_id.user.first_name + ' ' + m.manager_id.user.last_name,
                            'rate': percentage,
                            'id': m.city_id.id,
                            'brand_id': m.Brand_id.id,
                           }
                cityInfo.append(cityRow)
                sorted_data = sorted(cityInfo, key=lambda x: x['rate'], reverse=True)
                # chart data
                perlist.append(percentage)
                citieslist.append(m.city_id.name )

               
    #print(cityInfo)
    data = {
        # بيانات المدن ونتائجها
        'cityMangers' : sorted_data, 
        # بيانات للشارت 
        'perlist':perlist ,
        'citieslist':json.dumps(citieslist) ,

    }
    return render(request , 'brands/citiesRate.html' , data) 

# باقي تطلع النتايج
def districts_rate(request , id , brand_id):
    distlist=[]
    perlist=[]
    disrow=[]
    districts = District.objects.filter(city_id = id)
   
    for d in districts:
        final_score = branchs_dist_resault(d.id , brand_id)
        print(len(final_score))
        total = 0
        score_list = []
        for fs in final_score:
            score_list.append(int(fs['score'])) 
        for sl in score_list:
            total += sl
        #print(len(score_list))
        if len(score_list) == 0 :
            row = {
            
            }
        else :
            percentage = int((total / len(score_list)) )

        #############################################
            row = {
                'districtName' : d.name ,
                'rate' : percentage ,
                'id' : d.id,
                'brand_id' : brand_id,
            }
            distlist.append(row)
            perlist.append(percentage)
            disrow.append(d.name)
            
            sorted_data = sorted(distlist, key=lambda x: x['rate'], reverse=True)
    print(distlist)
    #print(distlist)
    data={
        'distInfo' : sorted_data,
        'perlist' : perlist,
        'disrow' : json.dumps(disrow),
    }
    return render(request , 'brands/distRate.html' , data) 


# فنكشن تفتح صفحه تقييم الفروع 
def branchs_rate(request , id , brand_id):
    # id  تبع الحي
    branchsInfo = []
    branchs = Branch.objects.filter(district_id = id , brand_id = brand_id)
    for br in branchs:
        final_score = branchs_percentage(br.id)
        total = 0
        score_list = []
        for fs in final_score:
            score_list.append(int(fs['score'])) 
        for sl in score_list:
            total += sl
        #print(len(score_list))
        if len(score_list) == 0 :
            percentage = 0
        else :
             percentage = int((total / len(score_list)) )

        #############################################
        print(final_score)
        row = {
            'branchName' : br.description ,
            'mngName' : br.manager_id,
            'rate' : percentage,
            'id' : br.id
        }
        branchsInfo.append(row)
        sorted_data = sorted(branchsInfo, key=lambda x: x['rate'], reverse=True)

    data = {
        'row' : sorted_data,
    }
    return render(request , 'brands/branchsRate.html' , data )


def reports_list(request , id):
    print(id)
    reportsInfo = []
    reports = Report_order.objects.filter(bransh_id = id)
    for ro in reports:
        resualt = Score_history.objects.get(report_order_id = ro.id)
        row = {
            'reportDate': ro.registerDate , 
            'rate' : resualt.total_score ,
            'id' : ro.id ,
        }
        reportsInfo.append(row)
    data = {
        'row' : reportsInfo
    }
    return render(request , 'brands/reportList.html' , data)

def show_report(request , id):
    scores = Term_score.objects.filter( report_order_id =id)
    history = Score_history.objects.get(report_order_id = id)
    # manager info
    order = Report_order.objects.get(id = id)
    mngName = order.bransh_id.manager_id
    print(mngName)
    mngEmail = mngName.user.email
    mngrs = Managers.objects.get(user_id = mngName.user.id)
    mngMobile = mngrs.mobile
    #print(scores)
    percentage = history.total_score
    term_result = []
    for score in scores:  
        if score.score == '1' :
            s = 'نعم'
            custom = 'badge-light-success'
        elif score.score == '0' :
            s = 'لا'
            custom = 'badge-light-danger'
        else : 
            s = 'مستبعد'
            custom = 'badge-light-primary'
        row = {
                    'description': score.term_id.description,
                    'score' : s ,
                    'note': score.note ,
                    'id': score.term_id.id,
                    'img' : str(score.img) ,
                    'class': custom ,
                    }
        term_result.append(row)
        print(term_result)
    data = {
        'row': term_result,
        'rate' : percentage ,
        'mngName' : mngName ,
        'mngEmail': mngEmail,
         'mngMobile': mngMobile ,
        }
    #print(term_result)
    return render(request , 'brands/report.html' , data)


    
######################################################################
######################################################################
################                                    ##################
######################################################################
######################################################################



def region_branches(region_id , brand_id):
    branchs_ids = []
    cities = City.objects.filter(region_id = region_id)
    for city in cities :
       districts = District.objects.filter(city_id = city.id)
       for district in districts :
            branches = Branch.objects.filter(district_id = district.id , brand_id = brand_id)# اصلاح رقم الايدي لليوزر
            for branch in branches:
                row = {
                    'brancheID' : branch.id
                }
                branchs_ids.append(row)
    return branchs_ids

# هذي الفنكشن تطلع نتائج الفروع اللي بالمناطق
def branchs_resault(region_id , brand_id):
    branches = region_branches(region_id , brand_id)
    #print(type(branches))
    repo =[]
    for br in branches:
        report_orders = Report_order.objects.filter(bransh_id = br['brancheID'])
        for ro in report_orders :
            score_his = Score_history.objects.filter(report_order_id = ro.id)
            for score in score_his:
                row ={
                    'score': score.total_score
                    }
                repo.append(row)          
    return repo


# هذي الفنكشن تطلع الفروع اللي بالمدن
def city_branches(city_id , brand_id):
    branchs_ids = []
    cities = City.objects.filter(id = city_id)
    for city in cities :
       districts = District.objects.filter(city_id = city.id)
       for district in districts :
            branches = Branch.objects.filter(district_id = district.id , brand_id = brand_id)
            print(branches)
            for branch in branches:
                row = {
                    'brancheID' : branch.id
                }
                branchs_ids.append(row)
    return branchs_ids

def branchs_city_resault(city_id , brand_id):
    branches = city_branches(city_id , brand_id)
    #print(type(branches))
    repo =[]
    for br in branches:
        report_orders = Report_order.objects.filter(bransh_id = br['brancheID'])
        for ro in report_orders :
            score_his = Score_history.objects.filter(report_order_id = ro.id)
            for score in score_his:
                row ={
                    'score': score.total_score
                    }
                repo.append(row)          
    return repo

################################3
def district_branches(dist_id , brand_id):
    branchs_ids = []
    districts = District.objects.filter(id = dist_id)
    for district in districts :
        branches = Branch.objects.filter(district_id = district.id , brand_id = brand_id)
        for branch in branches:
            row = {
                'brancheID' : branch.id
            }
            branchs_ids.append(row)
    return branchs_ids

def branchs_dist_resault(dist_id , brand_id):
    branches = district_branches(dist_id , brand_id)
    #print(type(branches))
    repo =[]
    for br in branches:
        report_orders = Report_order.objects.filter(bransh_id = br['brancheID'])
        for ro in report_orders :
            score_his = Score_history.objects.filter(report_order_id = ro.id)
            for score in score_his:
                row ={
                    'score': score.total_score
                    }
                repo.append(row)          
    return repo 

def branchs_percentage(branch_id):
    repo = []
    report_orders = Report_order.objects.filter(bransh_id = branch_id)
    for ro in report_orders :
        score_his = Score_history.objects.filter(report_order_id = ro.id)
        for score in score_his:
            row ={
                'score': score.total_score
                }
            repo.append(row)          
    return repo