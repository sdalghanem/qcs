from django.shortcuts import redirect, render
from .models import *
from report.models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
from datetime import datetime
from clients.dashboard_view import *
# Create your views here.
def regions_rate(request , id , y, q):
    #id for brand
    if request.user.is_authenticated:
        if request.method =='POST':
            return redirect('regions_rate' ,id = id, y = request.POST['year'] , q= request.POST['quarter'])
        else:
            cities =[]
            regioninfo =[]
            perlist=[]
            regionlist =[]
            chartList =[]
            mngs = Brand_regionManager.objects.filter(Brand_id = id )
            ### 
            branList = Brand.objects.filter(company_id = request.session['company_id'])
            current_year = datetime.now().year
            years = list(range(current_year, current_year - 10, -1))  # السنوات من السنة الحالية ولمدة 10 سنوات سابقة

            #final_score = Score_history.objects.filter(report_order_id=specific_id_value).latest('registerDate')
            brandName = ''
            brandLogo = ''
            
            for mng in mngs: 
                # اسم البرانج و اللوجو استخراج
                brandName = mng.Brand_id.description
                brandLogo = str(mng.Brand_id.logo)
                #print(brandLogo)
                #print(brandName)
                ############################################
                final_score = branchs_resault(mng.region_id , mng.Brand_id , y , q)
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
                    row = {
                    'name' : mng.manager_id.user.first_name + ' ' + mng.manager_id.user.last_name,
                    'region' : mng.region_id.name,
                    'rate': percentage,
                    'id' : mng.region_id.id , # id  المنطقة
                    'brand_id' : mng.Brand_id.id
                    }
                    regioninfo.append(row)
                    #perlist.append(percentage)
                    #regionlist.append(mng.region_id.name )
                    chartList.append({'name' :mng.region_id.name , 'perc' : percentage})
                    
                    cities.append(city_dashboard(mng.region_id.id ,mng.Brand_id.id , y , q ))  
                #############################################
            sorted_data = sorted(regioninfo, key=lambda x: x['rate'], reverse=True)
            chlist = sorted(chartList, key=lambda x: x['perc'], reverse=True)
            #print(chlist)
            allRegionScore = get_order_ids(id = id , y = y , q = q) # هذا نسبة الربع الاول
            # تشييك البراند اذا موجود او لا 
            if request.session['position'] == '0':
                mngBrand = ''
            else :
                mngBrand = request.session['brand_id']

            data = {
                'row': sorted_data,
                'chlist' : json.dumps(chlist),
                'cities': cities, 
                #'perlist':perlist ,
                #'regionlist':json.dumps(regionlist) ,
                'brandName' :brandName ,
                'brandLogo' :brandLogo ,
                'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
                'mngPostion' : return_JobTitle(request.session['position']) ,
                'mngBrand' :mngBrand,
                'companyLogo': request.session['companylogo'],
                'companyName': request.session['companyName'] ,
                'menubrands': branList ,
                'years' : years ,
                'y': y,
                'q': q,
                'brandMng': Brand.objects.get(id = id).gm_manager_id ,
                'allRegionScore' : allRegionScore,
                'position': request.session['position'] 
            }
        
            print(regionlist)
            return render(request , 'brands/regionsRate.html' , data)
    else:
        return render(request , 'login.html')

# هذي الفنكشن تعطيها رقم البوزشن ويرجع لك اسم المنصب كتابة
def return_JobTitle(postion):
    if postion == '0':
        return 'مدير عام'
    elif postion == '1':
        return 'مدير علامة تجارية'
    elif postion == '2':
        return 'مدير منطقة'
    elif postion == '3':
        return 'مدير مدينة'
    elif postion == '4':
        return 'مدير فرع'
    elif postion == '5':
        return 'مدير إدارة'
    
def city_dashboard(region_id , brand_id , y , q):
      #id = region id
    # اول شي تجيب المدن اللي بوسط المنطقة
    cities = City.objects.filter(region_id_id = region_id)
    cityInfo = []
    for c in cities:
        # ثاني شي تجيب اسامي المدراء
        if Brand_cityManager.objects.filter(Brand_id = brand_id , city_id = c.id).exists():
            mngs = Brand_cityManager.objects.filter(Brand_id = brand_id , city_id = c.id) #  اصلاح رقم اي دي العلامه التجارية
            for m in mngs:
                final_score = branchs_city_resault(m.city_id.id , m.Brand_id.id , y , q)
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
        row ={
            'brand_id': brand_id,
            'regionName': c.region_id.name ,
            'regid': c.region_id.id,
            'cities':cityInfo ,
        }
         # sorted_data = sorted(cityInfo, key=lambda x: x['rate'], reverse=True)
    return row
               

# فنكشن لتقييم المدن
def cities_rate(request , id ,brand_id , y , q):
    #id = region id
    if request.user.is_authenticated:
        if request.method =='POST':
            return redirect('cities_rate' , id = id , brand_id = brand_id , y = request.POST['year'] , q = request.POST['quarter'])
            # اول شي تجيب المدن اللي بوسط المنطقة
        else:
            cities = City.objects.filter(region_id = id)
            cityInfo = []
            # chart data
            #perlist=[]
            citieslist=[]
            
            for c in cities:
                # ثاني شي تجيب اسامي المدراء
                if Brand_cityManager.objects.filter(Brand_id = brand_id , city_id = c.id).exists():
                    mngs = Brand_cityManager.objects.filter(Brand_id = brand_id , city_id = c.id) #  اصلاح رقم اي دي العلامه التجارية
                    for m in mngs:
                        final_score = branchs_city_resault(m.city_id.id , m.Brand_id.id , y , q)
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
                        
                        # chart data
                        #perlist.append(percentage)
                        citieslist.append({'cityName': m.city_id.name , "perc": percentage} )
                    sorted_data = sorted(cityInfo, key=lambda x: x['rate'], reverse=True)
                    
            #print(cityInfo)
            current_year = datetime.now().year
            years = list(range(current_year, current_year - 10, -1))  # السنوات من السنة الحالية ولمدة 10 سنوات سابقة
            
            # حساب 
            final_score = branchs_resault(id , brand_id , y , q)
            total = 0
            percentage_r = 0
            score_list = []
            for fs in final_score:
                score_list.append(int(fs['score'])) 
            for sl in score_list:
                total += sl
            if len(score_list) == 0 :
                percentage_r = 0
            else :
                percentage_r = int((total / len(score_list)) )
            #################################
            if request.session['position'] == '0':
                mngBrand = ''
            else :
                mngBrand = request.session['brand_id']

            data = {
                'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
                'mngPostion' : return_JobTitle(request.session['position']) ,
                'companyLogo': request.session['companylogo'],
                'companyName': request.session['companyName'] ,
                'menubrands': Brand.objects.filter(company_id = request.session['company_id']) ,
                'brandName': Brand.objects.get(id = brand_id ).description ,
                'brandLogo' :  Brand.objects.get(id = brand_id ).logo,
                'brand_id': brand_id ,
                # بيانات المدن ونتائجها
                'cityMangers' : cityInfo, 
                # بيانات للشارت 
                #'perlist':perlist ,
                'citieslist':json.dumps(citieslist) ,
                'y' : y,
                'q': q,
                'mngBrand' : mngBrand ,
                'years' : years,
                'regionName': Region.objects.get(id = id).name ,
                'regRate': percentage_r ,
                'position': request.session['position'] ,

            }
            return render(request , 'brands/citiesRate.html' , data) 
    else:
        return render(request , 'login.html')

# باقي تطلع النتايج
def districts_rate(request , id , brand_id , y, q ):
    # id for city id
    if request.user.is_authenticated:
        if request.method =='POST':
            return redirect('districts_rate' , id= id ,brand_id = brand_id , y = request.POST['year'] , q = request.POST['quarter'] )
        else :
            distlist=[]
            perlist=[]
            disrow=[]
            districts = District.objects.filter(city_id = id)
            sorted_data = ''
            for d in districts:
                final_score = branchs_dist_resault(d.id , brand_id , y , q)
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
                    #perlist.append( percentage)
                    disrow.append({'disName':d.name , 'perc': percentage})
                    
                    sorted_data = sorted(distlist, key=lambda x: x['rate'], reverse=True)
            print(distlist)
            #print(distlist)
            current_year = datetime.now().year
            years = list(range(current_year, current_year - 10, -1))  # السنوات من السنة الحالية ولمدة 10 سنوات سابقة

            ## نسبة المدينه للعرض بالدائرة 
            final_score_city = branchs_city_resault(id, brand_id , y , q)
            total_city = 0
            score_list_city = []
            for fs in final_score_city:
                score_list_city.append(int(fs['score'])) 
            for sl in score_list_city:
                total_city += sl
            #print(len(score_list))
            if len(score_list) == 0 :
                percentage_city = 0
            else :
                    percentage_city = int((total_city / len(score_list_city)) )
            #################################
            #################################
            if request.session['position'] == '0':
                mngBrand = ''
            else :
                mngBrand = request.session['brand_id']
            data={
                'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
                'mngPostion' : return_JobTitle(request.session['position']) ,
                'companyLogo': request.session['companylogo'],
                'companyName': request.session['companyName'] ,
                'menubrands': Brand.objects.filter(company_id = request.session['company_id']) ,
                'brandName': Brand.objects.get(id = brand_id ).description ,
                'brandLogo' :  Brand.objects.get(id = brand_id ).logo,
                ########################
                'distInfo' : sorted_data,
                'perlist' : perlist,
                'disrow' : json.dumps(disrow),
                'y' : y ,
                'q': q,
                'years' : years,
                'brand_id': brand_id,
                'regionName': City.objects.get(id = id).region_id.name,
                'region_id': City.objects.get(id = id).region_id.id,
                'cityName': City.objects.get(id = id).name,
                'percentage_city' : percentage_city,
                'position': request.session['position'] ,
                'mngBrand': mngBrand

            }
            return render(request , 'brands/distRate.html' , data) 
    else:
            return render(request , 'login.html')


# فنكشن تفتح صفحه تقييم الفروع 
def branchs_rate(request , id , brand_id , y , q):
    # id  تبع الحي
    if request.user.is_authenticated:
        if request.method =='POST':
            return redirect('branchs_rate' , id= id ,brand_id = brand_id , y = request.POST['year'] , q = request.POST['quarter'] )
        else:
            branchsInfo = []
            branchs = Branch.objects.filter(district_id = id , brand_id = brand_id)
            for br in branchs:
                final_score = branchs_percentage(br.id , y , q)
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
            current_year = datetime.now().year
            years = list(range(current_year, current_year - 10, -1))  # السنوات من السنة الحالية ولمدة 10 سنوات سابقة

            #################################
            if request.session['position'] == '0':
                mngBrand = ''
            else :
                mngBrand = request.session['brand_id']

            data = {
                'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
                'mngPostion' : return_JobTitle(request.session['position']) ,
                'companyLogo': request.session['companylogo'],
                'companyName': request.session['companyName'] ,
                'menubrands': Brand.objects.filter(company_id = request.session['company_id']) ,
                'brandName': Brand.objects.get(id = brand_id ).description ,
                'brandLogo' :  Brand.objects.get(id = brand_id ).logo,
                'disName' : District.objects.get(id = id).name ,
                ########################
                'row' : sorted_data,
                'y' : y,
                'q': q,
                'years': years,
                'brand_id': brand_id,
                'region_id': District.objects.get(id = id).city_id.region_id.id,
                'regionName': District.objects.get(id = id).city_id.region_id.name,
                'cityName': District.objects.get(id = id).city_id.name,
                'city_id': District.objects.get(id = id).city_id.id,
                'position': request.session['position'] ,
                'mngBrand': mngBrand



            }
            return render(request , 'brands/branchsRate.html' , data )
    else:
        return render(request , 'login.html')

def reports_list(request , id , y , q):
    # id for branch
    if request.user.is_authenticated:
        if request.method =='POST':
             return redirect('reports_list' , id= id , y = request.POST['year'] , q = request.POST['quarter'] )
        else:
            reportsInfo = []
            if q == '0':
                  reports = Report_order.objects.filter(bransh_id = id , year = y  ,  status = '3' )
            else:
                reports = Report_order.objects.filter(bransh_id = id , year = y  , quarter = q , status = '3' )
            for ro in reports:
                if Score_history.objects.filter(report_order_id = ro.id).exists():
                    resualt = Score_history.objects.get(report_order_id = ro.id)
                    row = {
                        'reportDate': ro.registerDate , 
                        'rate' : resualt.total_score ,
                        'id' : ro.id ,
                        'quarter' : ro.quarter,
                    }
                    reportsInfo.append(row)
                
            current_year = datetime.now().year
            years = list(range(current_year, current_year - 10, -1))  # السنوات من السنة الحالية ولمدة 10 سنوات سابقة
            #################################
            if request.session['position'] == '0':
                mngBrand = ''
            else :
                mngBrand = request.session['brand_id']
            data = {
                'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
                'mngPostion' : return_JobTitle(request.session['position']) ,
                'companyLogo': request.session['companylogo'],
                'companyName': request.session['companyName'] ,
                'menubrands': Brand.objects.filter(company_id = request.session['company_id']) ,
                'brandName': Branch.objects.get(id = id ).brand_id.description ,
                'brandLogo' :  Branch.objects.get(id = id ).brand_id.logo,
                'brand_id' :  Branch.objects.get(id = id ).brand_id.id,
                'branchName' : Branch.objects.get(id = id ).description ,
                'branchMng' : Branch.objects.get(id = id ).manager_id ,
                'branchEmail' : Branch.objects.get(id = id ).manager_id.user.email ,
                'branchMobile' : Branch.objects.get(id = id ).manager_id.mobile ,
                'region_id':Branch.objects.get(id = id ).district_id.city_id.region_id.id,
                'regionName':Branch.objects.get(id = id ).district_id.city_id.region_id.name,
                'city_id':Branch.objects.get(id = id ).district_id.city_id.id,
                'cityName':Branch.objects.get(id = id ).district_id.city_id.name,
                'disName': Branch.objects.get(id = id ).district_id.name,
                'dist_id': Branch.objects.get(id = id ).district_id.id,
                ########################
                'row' : reportsInfo,
                'y': y,
                'q': q,
                'years': years,
                'position': request.session['position'] ,
                'mngBrand': mngBrand

            }
            return render(request , 'brands/reportList.html' , data)
    else:
        return render(request , 'login.html')


def show_report(request , id):
    # id for report order 
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
    current_year = datetime.now().year
    #################################
    if request.session['position'] == '0':
        mngBrand = ''
    else :
                mngBrand = request.session['brand_id']
    data = {
        'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
        'mngPostion' : return_JobTitle(request.session['position']) ,
        'companyLogo': request.session['companylogo'],
        'companyName': request.session['companyName'] ,
        'menubrands': Brand.objects.filter(company_id = request.session['company_id']) ,
        'brandName': Report_order.objects.get(id = id ).bransh_id.brand_id.description ,
        'brandLogo' :  Report_order.objects.get(id = id ).bransh_id.brand_id.logo,
        'brand_id' :  Report_order.objects.get(id = id ).bransh_id.brand_id.id,
        'regionName' :  Report_order.objects.get(id = id ).bransh_id.district_id.city_id.region_id.name,
        'region_id' :  Report_order.objects.get(id = id ).bransh_id.district_id.city_id.region_id.id,
        'disName':  Report_order.objects.get(id = id ).bransh_id.district_id.name,
        'dist_id':  Report_order.objects.get(id = id ).bransh_id.district_id.id,
        'city_id': Report_order.objects.get(id = id ).bransh_id.district_id.city_id.id,
        'cityName': Report_order.objects.get(id = id ).bransh_id.district_id.city_id.name,
        'branchName' : Report_order.objects.get(id = id ).bransh_id.description,
        'branch_id' : Report_order.objects.get(id = id ).bransh_id.id,

        ########################

        'row': term_result,
        'rate' : percentage ,
        'mngName2' : mngName ,
        'mngEmail': mngEmail,
         'mngMobile': mngMobile ,
         'y': current_year ,
         'q': 'q1',
         'reportid' : id ,
         'position': request.session['position'] ,
        'mngBrand': mngBrand

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
def branchs_resault(region_id , brand_id , y , q):
    branches = region_branches(region_id , brand_id)
    #print(type(branches))
    repo =[]
    for br in branches:
        if q == '0':
            report_orders = Report_order.objects.filter(bransh_id = br['brancheID'] , year= y , status ='3')
        else :  
             report_orders = Report_order.objects.filter(bransh_id = br['brancheID'] , year= y , quarter = q , status ='3')
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

def branchs_city_resault(city_id , brand_id , y , q):
    branches = city_branches(city_id , brand_id)
    #print(type(branches))
    repo =[]
    for br in branches:
        if q == '0':
             report_orders = Report_order.objects.filter(bransh_id = br['brancheID'] , year=y , status = '3')
        else :
            report_orders = Report_order.objects.filter(bransh_id = br['brancheID'] , year=y , quarter = q , status = '3')
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

def branchs_dist_resault(dist_id , brand_id , y , q):
    branches = district_branches(dist_id , brand_id)
    #print(type(branches))
    repo =[]
    for br in branches:
        if q == '0':
             report_orders = Report_order.objects.filter(bransh_id = br['brancheID'] , year = y , status = '3')
        else:
            report_orders = Report_order.objects.filter(bransh_id = br['brancheID'] , year = y , quarter = q , status = '3')
        for ro in report_orders :
            score_his = Score_history.objects.filter(report_order_id = ro.id)
            for score in score_his:
                row ={
                    'score': score.total_score
                    }
                repo.append(row)          
    return repo 

def branchs_percentage(branch_id , y , q ):
    repo = []
    if q == '0':
         report_orders = Report_order.objects.filter(bransh_id = branch_id , year=y ,status = '3' )
    else:
        report_orders = Report_order.objects.filter(bransh_id = branch_id , year=y , quarter=q ,status = '3')
    for ro in report_orders :
        score_his = Score_history.objects.filter(report_order_id = ro.id)
        for score in score_his:
            row ={
                'score': score.total_score
                }
            repo.append(row)          
    return repo





##########################################################################################

def get_order_ids(id , y , q):
    print("اختبار قيمة الربع " + str(q))
    # id for brand y for year  q for quarter
    brnchs = Branch.objects.filter(brand_id_id = id)
    row = []
    for b in brnchs :
        if q == '0':
            ords = Report_order.objects.filter(bransh_id_id = b.id , status = '3' , year = y )
        else :
            ords = Report_order.objects.filter(bransh_id_id = b.id , status = '3' , year = y , quarter = q)
        for o in ords:
            row.append(o.id)
    percentage = calculate_average_percentage(row)
    return percentage

def calculate_average_percentage(report_order_ids):
    # جلب السجلات بناءً على قائمة report_order_ids
    score_histories = Score_history.objects.filter(report_order_id__in=report_order_ids)

    # التحقق من وجود درجات
    if not score_histories.exists():
        return 0  # لا توجد بيانات لحساب المتوسط

    # حساب مجموع الدرجات وتحويلها إلى أعداد صحيحة
    total_score_sum = 0
    count = 0

    for score_history in score_histories:
        try:
            # تحويل الدرجة إلى عدد صحيح
            total_score_sum += int(score_history.total_score)
            count += 1
        except ValueError:
            # تجاهل السجلات التي لا تحتوي على درجات صحيحة
            continue

    # حساب متوسط الدرجات
    average_score = total_score_sum / count if count > 0 else 0

    # حساب النسبة المئوية (لنفترض أن أقصى درجة هي 100)
    average_percentage = (average_score / 100) * 100

    return int(average_percentage)  # تحويل النسبة إلى عدد صحيح