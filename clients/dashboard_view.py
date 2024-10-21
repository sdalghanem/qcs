from django.shortcuts import redirect, render
from .models import *
from report.models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate , login as auth_login , logout
from .departments_view import *
from datetime import datetime
from .brands_view import *
##
# تخصص كل لوحة تحكم لكل منصب باقي

# صفحة دخول لوحة التحكم للمدير العام
def gm_dashboard(request , y , q):
    if request.user.is_authenticated:
        if request.method =='POST':
            return redirect('gm_dashboard' , y = request.POST['year'] , q= request.POST['quarter'])
        else:
            row = []
            brands = Brand.objects.filter(company_id = request.session['company_id'])
            brandsList = []

        # # # # هنا لوب البراندات تحط فيه اللي تبيه يظهر
            for b in brands:
                brandName = b.description
                brandid = b.id
                #### الادارات
                depts = calc_departmet(request , id =brandid , y = y , q = q)
                deptslast = calc_departmetlast(request , id =brandid , y = y , q = q)
                #### المناطق
                regionsRates = calc_regions(b.id , y , q)
                regionsRates_last = calc_regions_last(b.id , y , q)
                ####### الفروع
                branchs = calc_branchs(b.id , y , q)
                branchs_last = calc_branchs_last(b.id , y , q)

                print(branchs)
                #########
                perc = int(get_order_ids(id =brandid , y = y , q = q)) # هذا نسبة الربع الاول
                row = {
                    'brandName' : brandName ,
                    'brandid' : brandid,
                    'logo': b.logo ,
                    'perc': perc ,
                    'depts' : depts ,
                    'regionsRates' : regionsRates,
                    'branchs' : branchs,
                    'y': y,
                    'q':q ,
                    'deptslast':deptslast,
                    'regionsRates_last':regionsRates_last,
                    'branchs_last': branchs_last,
                }
                brandsList.append(row)
        # السنوات
            current_year = datetime.now().year
            years = list(range(current_year, current_year - 10, -1))  # السنوات من السنة الحالية ولمدة 10 سنوات سابقة
            data = {
                'menubrands' : brandsList,
                'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
                'mngPostion' : 'مدير عام' ,
                'companyName' : request.session['companyName'],
                'companyLogo': request.session['companylogo'],
                'brands' : brands,
                'years': years,
                'y': y,
                'q':q,
            }
            return render(request , 'dashboards/dashboard.html' , data)
    else:
        return render(request , 'login.html')
    

def calc_departmet(request ,id , y , q):
    #id for company
    deptInfoList = []
    row=[]
    sections = Section.objects.filter( Brand_id_id = id)
    for s in sections:
        listdept =  get_sec_terms(s.id)# تجيب لسته البنود
        percentage = calculate_percentage_for_orders(get_orders_by_brand(s.Brand_id.id ,y , q) , listdept)
        row = {
            'departmentName' : s.description,
            'percentage': int(percentage) ,#per, #Company ,
        }
        deptInfoList.append(row)
        
    sorted_data = sorted(deptInfoList, key=lambda x: x['percentage'], reverse=True)
    return sorted_data[:3]

def calc_departmetlast(request, id, y, q):
    # id for company
    deptInfoList = []
    
    sections = Section.objects.filter(Brand_id_id=id)
    
    for s in sections:
        listdept = get_sec_terms(s.id)  # تجيب لسته البنود
        percentage = calculate_percentage_for_orders(get_orders_by_brand(s.Brand_id.id, y, q), listdept)
        
        row = {
            'departmentName': s.description,
            'percentage': int(percentage),  # تحويل النسبة إلى عدد صحيح
        }
        
        deptInfoList.append(row)
    
    # ترتيب البيانات حسب النسبة المئوية تصاعدياً
    sorted_data = sorted(deptInfoList, key=lambda x: x['percentage'])
    
    # إرجاع أقل 3 نتائج فقط
    return sorted_data[:3]

##############################
def get_orders_by_brand(id , y , q):
    # هذا الفنكشن يقوم بارجاع لسته الطلبات بناء على العلامة التجارية بالربع السنوي المحدد
    orlist= []
    branchs = Branch.objects.filter(brand_id_id = id)
    for bh in branchs:           
        orders = Report_order.objects.filter(bransh_id_id =  bh.id , year =y , quarter = q) 
        for o in orders :
            orlist.append(o.id)
    return orlist
## حساب المناطق بناء على البراند اي دي و الربع
def calc_regions(id ,y , q):
     # id for brand
    region_scores = []  # قائمة لتخزين السكور لكل منطقة
    regions = Region.objects.all()

    for r in regions:
        depName = r.name
        total_region_score = 0  # متغير لتجميع السكور الخاصة بكل منطقة
        branches = region_branches(r.id, id)

        for br in branches:
            report_orders = Report_order.objects.filter(bransh_id=br['brancheID'] , year = y , quarter = q)

            for ro in report_orders:
                score_his = Score_history.objects.filter(report_order_id=ro.id)

                for score in score_his:
                    # تحويل total_score إلى int للتأكد من عدم وجود مشاكل في الإضافة
                    try:
                        total_region_score += int(score.total_score)
                    except ValueError:
                        # إذا كانت القيمة لا يمكن تحويلها إلى int، يتم تجاهلها أو التعامل معها
                        pass

        # إضافة اسم المنطقة ومجموع السكور إلى قائمة النتيجة
        region_scores.append({
            'region_name': depName,
            'region_score': total_region_score
        })
    sorted_data = sorted(region_scores, key=lambda x: x['region_score'], reverse=True)
    return sorted_data[:3]

def calc_regions_last(id ,y , q):
     # id for brand
    region_scores = []  # قائمة لتخزين السكور لكل منطقة
    regions = Region.objects.all()

    for r in regions:
        depName = r.name
        total_region_score = 0  # متغير لتجميع السكور الخاصة بكل منطقة
        branches = region_branches(r.id, id)

        for br in branches:
            report_orders = Report_order.objects.filter(bransh_id=br['brancheID'] , year = y , quarter = q)

            for ro in report_orders:
                score_his = Score_history.objects.filter(report_order_id=ro.id)

                for score in score_his:
                    # تحويل total_score إلى int للتأكد من عدم وجود مشاكل في الإضافة
                    try:
                        total_region_score += int(score.total_score)
                    except ValueError:
                        # إذا كانت القيمة لا يمكن تحويلها إلى int، يتم تجاهلها أو التعامل معها
                        pass

        # إضافة اسم المنطقة ومجموع السكور إلى قائمة النتيجة
        region_scores.append({
            'region_name': depName,
            'region_score': total_region_score
        })
    sorted_data = sorted(region_scores, key=lambda x: x['region_score'])
    return sorted_data[:3] 

def calc_branchs(id , y , q):
  # id  تبع العلامة التجارية
    branchsInfo = []
    branchs = Branch.objects.filter(brand_id = id)
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
            'rate' : percentage,
        }
        branchsInfo.append(row)
    sorted_data = sorted(branchsInfo, key=lambda x: x['rate'], reverse=True)
    return sorted_data[:3]

def calc_branchs_last(id , y , q):
  # id  تبع العلامة التجارية
    branchsInfo = []
    branchs = Branch.objects.filter(brand_id = id)
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
            'rate' : percentage,
        }
        branchsInfo.append(row)
    sorted_data = sorted(branchsInfo, key=lambda x: x['rate'])
    return sorted_data[:3]   
    ###########################################################################################
##################################################################################################
def get_order_ids(id , y , q):
    # id for brand y for year  q for quarter
    brnchs = Branch.objects.filter(brand_id_id = id)
    row = []
    for b in brnchs :
        ords = Report_order.objects.filter(bransh_id_id = b.id , status = '2' , year = y , quarter = q)
        for o in ords:
            row.append(o.id)
    percentage = calculate_average_percentage(row)
    print(type(percentage))
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
################################################################################################
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

