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
    departments = Department.objects.filter(company_id = 1)
    for d in departments:
        per = 0
        listdept =  get_dept_terms(d.id)# تجيب لسته البنود
        listscore = get_score(listdept)# تجيب لسته نتايج الاداره بناء على لسته البنود 
        total = 0
        for lis in listscore:
            total += int(lis['score'])
            if len(listscore) == 0 :
                per = 0
            else:
                per = int(total *100 / len(listscore))
        row = {
            'departmentName' : d.description,
            'percentage': per, #Company ,
            'id' : d.id,
        }
        deptInfoList.append(row)
        perlist.append(per)
        infolist.append(d.description)
        
    sorted_data = sorted(deptInfoList, key=lambda x: x['percentage'], reverse=True)
    data = {
       #'departments' : deptName,
       'row' : sorted_data, #  معلومات الادارات
       'perlist': perlist,
       'infolist':json.dumps(infolist) ,
        }
    return render(request , 'departments/deptsRate.html' , data) 

####################################################################################

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
def get_dept_terms(dept_id):
    row = []
    sections = Section.objects.filter(department_id = dept_id)
    for s in sections :
        terms = Term_responsible.objects.filter(section_id = s.id)
        for t in terms:
            terminfo = {
                'termid' : t.term_id.id,
            }
            row.append(terminfo)
    return row

# فنكشن تعطيه اي دي الاداره ويرجع لك لسته اي دي البنود التابعه له
def get_sec_terms(secid):
    row = []
    terms = Term_responsible.objects.filter(section_id = secid)
    for t in terms:
        terminfo = {
            'termid' : t.term_id.id,
            'tname' : t.term_id.description,
        }
        row.append(terminfo)
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