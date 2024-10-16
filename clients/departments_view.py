from django.shortcuts import render
from .models import *
from report.models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
from report.views import *
from .brands_view import *

def departments_rate(request):
    #deptName = []
    deptInfoList = []
    perlist = []
    infolist =[]
    departments = Department.objects.filter(company_id = request.session['company_id'])
    for d in departments:
        per = 0
        listdept =  get_dept_terms(d.id)# تجيب لسته البنود
        listscore = calculate_percentage_for_orders(get_orders_by_company(request.session['company_id'] ,'2024' , 'q1') ,listdept)# تجيب لسته نتايج الاداره بناء على لسته البنود 
        # total = 0
        # for lis in listscore:
        #     total += int(lis['score'])
        #     if len(listscore) == 0 :
        #         per = 0
        #     else:
        #         per = int(total *100 / len(listscore))
        row = {
            'departmentName' : d.description,
            'percentage': listscore ,#per, #Company ,
            'id' : d.id,
        }
        deptInfoList.append(row)
        perlist.append(listscore)
        infolist.append(d.description)
        
    #sorted_data = sorted(deptInfoList, key=lambda x: x['percentage'], reverse=True)
    data = {
       #'departments' : deptName,
       'row' : deptInfoList, #  معلومات الادارات
       'perlist': perlist,
       'infolist':json.dumps(infolist) ,
        }
    return render(request , 'departments/deptsRate.html' , data) 

def get_orders_by_company(id , y , q):
    # هذا الفنكشن يقوم بارجاع لسته الطلبات بناء على الشركة بالربع السنوي المحدد
    brands = Brand.objects.filter(company_id_id = id)
    orlist= []
    for bd in brands:
        branchs = Branch.objects.filter(brand_id_id = bd.id)
        for bh in branchs:           
            orders = Report_order.objects.filter(bransh_id_id =  bh.id , year =y , quarter = q) 
            for o in orders :
                orlist.append(o.id)
    return orlist
# ##############################################################################

def sections_rate(request , id):
    #i d for departments
    #deptName = []
    secList = []
    perlist = []
    infolist =[]
    sections = Section.objects.filter(department_id = id)
    
    for s in sections:
        per = 0
        listdept =  get_sec_terms(s.id)# تجيب لسته البنود
        listscore = get_score(listdept)# تجيب لسته نتايج القسم بناء على لسته البنود 
        total = 0
        for lis in listscore:
            total += int(lis['score'])
            if len(listscore) == 0 :
                per = 0
            else:
                per = int(total *100 / len(listscore))
        row = {
            'secName' : s.description,
            'percentage': per, #Company
            'id': s.id
        }
        secList.append(row)
        
        # row2={
        #     '':
        #     '' :
        # }
        perlist.append(per)
        infolist.append(s.description)
    sorted_data = sorted(secList, key=lambda x: x['percentage'], reverse=True)
    #sorted_per = sorted(perlist, key=lambda x: x['percentage'], reverse=True)
    data = {
       #'departments' : deptName,
       'row' : sorted_data, #  معلومات الاقسام
       'perlist': perlist,
       'infolist':json.dumps(infolist) ,
        }
    return render(request , 'departments/sectionsRate.html' , data) 
####################################################################################

def terms_rate(request , id):
    #i d for sections
    tlist = []
    termsList =  get_sec_terms(id)# تجيب لسته 
    for t in termsList:
      # listscore = get_score(t['termid'])
       result = get_result(t['termid'])
       for r in result:
           yes = len(r['yes'])
           no = len(r['no'])
           none = len(r['none']) 
       tlist.append({
                      'term':t['tname'] ,
                      'yes': yes ,
                      'no': no ,
                      'none': none,
                      })
    
    data = {
       #'departments' : deptName,
       'row' : tlist, #  معلومات الادارات
        }
    #print(data)
    return render(request , 'departments/termsRate.html' , data) 

def get_result(term_id):
    term_score = Term_score.objects.filter(term_id = term_id )
    scoreList = []
    yes = []
    no = []
    none = []
    for ts in term_score :
        if ts.score == '1' :
            yes.append(ts.score)
        elif ts.score == '0' :
            no.append(ts.score)
        else:
            none.append(ts.score)
        row = {
            'yes' : yes,
            'no' : no , 
            'none' : none,
        }
        scoreList.append(row)
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

def get_score(list):
    row = []
   
    # تستقبل لسته التيرم الخاصه بالاداره
    for l in list:
        tscores = Term_score.objects.filter( term_id = l['termid'])
        for t in tscores:
            score = {
                'score' : t.score ,
                #'term' : t.term_id.description ,
            }
            row.append(score)
            #print(row)
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
