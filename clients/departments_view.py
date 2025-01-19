from django.shortcuts import render
from .models import *
from report.models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
from report.views import *
from .brands_view import *

def departments_rate(request , y , q):
    if request.user.is_authenticated:
        if request.method =='POST':
            return redirect('departments_rate' , y = request.POST['year'] , q = request.POST['quarter'] )
        else:
            deptInfoList = []
            perlist = []
            infolist =[]
            departments = Department.objects.filter(company_id = request.session['company_id'])
            for d in departments:
                listdept =  get_dept_terms(d.id)# تجيب لسته البنود
                listscore = calculate_percentage_for_orders(get_orders_by_company(request.session['company_id'] ,y ,q) ,listdept)# تجيب لسته نتايج الاداره بناء على لسته البنود 
                row = {
                    'departmentName' : d.description,
                    'deptMng': d.manager_id,
                    'percentage': listscore ,#per, #Company ,
                    'id' : d.id,
                }
                deptInfoList.append(row)
                infolist.append({ 'deptName' :d.description , 'perc' :listscore })
            current_year = datetime.now().year
            years = list(range(current_year, current_year - 10, -1))  # السنوات من السنة الحالية ولمدة 10 سنوات سابقة
            # ترتيب من الاعلى الا الانتزل
            sorted_data = sorted(deptInfoList, key=lambda x: x['percentage'], reverse=True)
            sorted_data2 = sorted(infolist, key=lambda x: x['perc'], reverse=True)

            data = {
            'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
            'mngPostion' : 'مدير عام' ,
            'companyLogo': request.session['companylogo'],
            'menubrands': Brand.objects.filter(company_id = request.session['company_id']) ,
            'companyName': Company.objects.get(id = request.session['company_id']).description ,
            ########################
            'row' : sorted_data, #  معلومات الادارات
            'perlist': perlist,
            'infolist':json.dumps(sorted_data2) ,
            'y': y,
            'q': q,
            'years':years ,
                }
            return render(request , 'departments/deptsRate.html' , data) 
    else:
        return render(request , 'login.html')


def get_orders_by_company(id , y , q):
    # هذا الفنكشن يقوم بارجاع لسته الطلبات بناء على الشركة بالربع السنوي المحدد
    brands = Brand.objects.filter(company_id_id = id)
    orlist= []
    for bd in brands:
        branchs = Branch.objects.filter(brand_id_id = bd.id)
        for bh in branchs:  
            if q == '0' :
                orders = Report_order.objects.filter(bransh_id_id =  bh.id , year =y ) 
            else :
                orders = Report_order.objects.filter(bransh_id_id =  bh.id , year =y , quarter = q) 
            for o in orders :
                orlist.append(o.id)
    return orlist
# ##############################################################################

def sections_rate(request , id ,y , q):
    # id for department
    if request.user.is_authenticated:
        if request.method =='POST':
            return redirect('sections_rate' ,id = id, y = request.POST['year'] , q = request.POST['quarter'] )
        else:
            #i d for departments
            secList = []
            perlist = []
            infolist =[]
            sections = Section.objects.filter(department_id = id)
            for s in sections:
                per = 0
                listdept =  get_sec_terms(s.id)# تجيب لسته البنود
                listscore = get_score(listdept , y , q)# تجيب لسته نتايج القسم بناء على لسته البنود 
                total = 0
                for lis in listscore:
                    total += lis['score']
                    if len(listscore) == 0 :
                        per = 0
                    else:
                        per = round((total * 100) / len(listscore))
                row = {
                    'secName' : s.description,
                    'secMng' : s.manager_id,
                    'brandName': s.Brand_id,
                    'percentage': per, #Company
                    #'percentage': calculate_percentage_for_orders(get_score(listdept , y , q),get_sec_terms(s.id)),
                    'id': s.id
                }
                secList.append(row)
                perlist.append(per)
                infolist.append(s.description)
            sorted_data = sorted(secList, key=lambda x: x['percentage'], reverse=True)
            current_year = datetime.now().year 
            years = list(range(current_year, current_year - 10, -1))  # السنوات من السنة الحالية ولمدة 10 سنوات سابقة
            data = {
                'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
                'mngPostion' : 'مدير عام' ,
                'companyLogo': request.session['companylogo'],
                'menubrands': Brand.objects.filter(company_id = request.session['company_id']) ,
                'companyName': Company.objects.get(id = request.session['company_id']).description ,
                ########################
                'depName' : Department.objects.get(id = id).description,
                'row' : sorted_data, #  معلومات الاقسام
                'perlist': perlist,
                'infolist':json.dumps(infolist) ,
                'years': years,
                'y': y,
                'q': q,
                }
            print(Department.objects.get(id = id).description)
            return render(request , 'departments/sectionsRate.html' , data) 
    else:
        return render(request , 'login.html')

####################################################################################
def terms_rate(request, id , y , q):
    # i d for sections
        if request.user.is_authenticated:
            if request.method =='POST':
                return redirect('terms_rate' ,id = id, y = request.POST['year'] , q = request.POST['quarter'] )
            else:

                tlist = []

                termsList = get_sec_terms(id)  # تجيب لسته 
                for t in termsList:
                    # listscore = get_score(t['termid'])
                    result = get_result(t, y, q)

                    # تعيين قيم افتراضية للمتغيرات
                    yes, no, none = 0, 0, 0

                    for r in result:
                        yes = len(r.get('yes', []))  # التحقق من وجود المفتاح 'yes' وإلا نستخدم قائمة فارغة
                        no = len(r.get('no', []))    # التحقق من وجود المفتاح 'no' وإلا نستخدم قائمة فارغة
                        none = len(r.get('none', []))  # التحقق من وجود المفتاح 'none' وإلا نستخدم قائمة فارغة

                    tlist.append({
                        'term': Term.objects.get(id=t).description,
                        'yes': yes,
                        'no': no,
                        'none': none
                    })
                    print(len(tlist))

                current_year = datetime.now().year
                years = list(range(current_year, current_year - 10, -1))  # السنوات من السنة الحالية ولمدة 10 سنوات سابقة
                data = {
                    'mngName': request.session['firestName'] + ' ' + request.session['lastName'],
                    'mngPostion': 'مدير عام',
                    'companyLogo': request.session['companylogo'],
                    'menubrands': Brand.objects.filter(company_id=request.session['company_id']),
                    'companyName': Company.objects.get(id=request.session['company_id']).description,
                    ########################
                    'depName' : Section.objects.get(id = id).department_id.description,
                    'depid' : Section.objects.get(id = id).department_id.id,
                    'secName': Section.objects.get(id = id).description ,
                    'row': json.dumps(tlist),
                    'info': tlist,   # معلومات الادارات
                    'y': y,
                    'q': q,
                    'years': years,
                }
                # print(data)
                return render(request, 'departments/termsRate.html', data)
        else:
                return render(request , 'login.html')

# def terms_rate(request , id):
#     #i d for sections
#     tlist = []
    
#     termsList =  get_sec_terms(id)# تجيب لسته 
#     for t in termsList:
#       # listscore = get_score(t['termid'])
#         result = get_result(t , '2024' , 'q1')
#         for r in result:
#             yes = len(r['yes'])
#             no = len(r['no'])
#             none = len(r['none']) 
#         tlist.append({
#                       'term':Term.objects.get(id = t).description ,
#                       'yes': yes ,
#                       'no': no ,
#                       'none': none,
#                       })
#     current_year = datetime.now().year 
#     years = list(range(current_year, current_year - 10, -1))  # السنوات من السنة الحالية ولمدة 10 سنوات سابقة
#     data = {
#         'mngName' :  request.session['firestName'] + ' ' + request.session['lastName'] ,
#         'mngPostion' : 'مدير عام' ,
#         'companyLogo': request.session['companylogo'],
#         'menubrands': Brand.objects.filter(company_id = request.session['company_id']) ,
#         'companyName': Company.objects.get(id = request.session['company_id']).description ,
#         ########################
#        #'departments' : deptName,
#        'row' : tlist, #  معلومات الادارات
#        'y': '2024',
#        'q': 'q1',
#        'years': years,
#         }
#     #print(data)
#     return render(request , 'departments/termsRate.html' , data) 

# def get_result(term_id , y , q):
#     orders = Report_order.objects.filter(year = y , quarter = q)
#     for o in orders :
#         term_score = Term_score.objects.filter(term_id = term_id , report_order_id = o)
#         scoreList = []
#         yes = []
#         no = []
#         none = []
#         for ts in term_score :
#             if ts.score == '1' :
#                 yes.append(ts.score)
#             elif ts.score == '0' :
#                 no.append(ts.score)
#             else:
#                 none.append(ts.score)
#             row = {
#                 'yes' : yes,
#                 'no' : no , 
#                 'none' : none,
#             }
#             scoreList.append(row)
#     return scoreList
def get_result(term_id, y, q):
    if q == '0':
        orders = Report_order.objects.filter(year=y, )
    else:
        orders = Report_order.objects.filter(year=y, quarter=q)
    scoreList = []  # تأكد من تهيئة scoreList هنا خارج الحلقة
    yes = []
    no = []
    none = []
    for o in orders:
        term_score = Term_score.objects.filter(term_id=term_id, report_order_id=o)
        
       
        
        for ts in term_score:
            if ts.score == '1':
                yes.append(ts.score)
            elif ts.score == '0':
                no.append(ts.score)
            else:
                none.append(ts.score)
        
        # تأكد من أن row يتم إنشاؤه بعد التكرار الكامل على term_score
        row = {
            'yes': yes,
            'no': no,
            'none': none,
        }
        
        # إضافة النتيجة إلى scoreList
        scoreList.append(row)
        print('***************')
        print(scoreList)
    return scoreList

##################################################################################
# hellper functions ###
##################################################################################
# فنكشن تعطيه اي دي الاداره ويرجع لك لسته اي دي البنود التابعه له
def get_dept_terms(dept_id ):
    row = []
    sections = Section.objects.filter(department_id = dept_id )
    for s in sections :
        terms = Term_responsible.objects.filter(section_id = s.id)
        for t in terms:
           row.append(t.term_id.id)
    return row

# فنكشن تعطيه اي دي الاداره ويرجع لك لسته اي دي البنود التابعه له
def get_sec_terms(secid):
    row = []
    terms = Term_responsible.objects.filter(section_id = secid)
    for t in terms:
        # terminfo = {
        #     'termid' : t.term_id.id,
        #     'tname' : t.term_id.description,
        # }
        row.append(t.term_id.id)
    return row

def get_score(terms_list, y, q):
    row = []
    
    # جلب جميع الطلبات بناءً على السنة والربع
    if q == '0':
        orders = Report_order.objects.filter( year=y )
    else:
        orders = Report_order.objects.filter(year=y, quarter=q)
    
    # التكرار على قائمة البنود (terms_list)
    for order in orders:
        for l in terms_list:
        # التكرار على الطلبات لجلب درجات البند في كل طلب
       
            # جلب الدرجات بناءً على term_id والسنة والربع للطلب
            tscores = Term_score.objects.filter(term_id=l, report_order_id=order)
            
            # التكرار على جميع السجلات المطابقة
            for t in tscores:
                score = {
                    'score': int(t.score),
                    #'term': t.term_id.description,
                }
                row.append(score)

    return row



def calculate_percentage_for_orders(order_list, terms_list):
    # Initialize total score and total terms count
    overall_total_score = 0
    overall_total_terms = 0

    # Loop through each order in the order_list
    for order_id in order_list:
        # Get all Term_scores for this order and terms in the terms_list
        term_scores = Term_score.objects.filter(report_order_id=order_id, term_id__in=terms_list)

        # Initialize order-specific total score and count
        order_total_score = 0
        order_total_terms = len(terms_list)  # Total number of terms for this order
        
        # Sum the scores for each term in this order
        for term_score in term_scores:
            try:
                # Convert score to integer and add to order total score
                order_total_score += int(term_score.score)
            except ValueError:
                # Handle any invalid score (non-integer) gracefully
                continue       
        # Add the order's total score and terms to the overall total
        overall_total_score += order_total_score
        overall_total_terms += order_total_terms

    # Calculate overall percentage (if there are any terms)
    if overall_total_terms > 0:
        overall_percentage = (overall_total_score / overall_total_terms) * 100
    else:
        overall_percentage = 0
    
    # Return the rounded percentage as an integer
    return round(overall_percentage)
