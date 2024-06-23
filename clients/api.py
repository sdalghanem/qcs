from django.shortcuts import render
from .models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
from report.models import *
##
# from -> queries.html القائمة المنسدلة للمناطق 
# to  -> queries.html  القائمة المنسدله للمدن
# disc -> عند اختيار منطقة يتم استعراض المناطق
##
def cities_list(request):
    cities = City.objects.filter( region_id = request.POST['regionID'])
    data = list(cities.values()) 
    return JsonResponse( data , safe=False)

def district_list(request):
    districts = District.objects.filter( city_id = request.POST['cityID'])
    data = list(districts.values()) 
    return JsonResponse( data , safe=False)

def branch_list(request ):
    print(request.POST['brand_id'])
    branchs = Branch.objects.filter( district_id = request.POST['districtID'] , brand_id = request.POST['brand_id'])
    data = list(branchs.values()) 
    return JsonResponse( data , safe=False)

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# from -> queries.html القائمة المنسدلة للادارات#
# to  -> queries.html  القائمة المنسدله للاقسام
# disc -> عند اختيار الادارة يتم استعراض الاقسام
## 

def sections_list(request):
    sections = Section.objects.filter(department_id = request.POST['department_id'] )
    #print(departments)
    data = list(sections.values()) 
    return JsonResponse( data , safe=False)


def reports_list(request ):
    #print(request.POST['brand'])
    rolist = []
    if Report_order.objects.filter( bransh_id = request.POST['branch_id']).exists():
        orders = Report_order.objects.filter( bransh_id = request.POST['branch_id'])
        for order in orders:
            row = {'date' : order.registerDate ,
                    'id' : order.id ,
                    'branch' : order.bransh_id.description ,}
            rolist.append(row)
    # تروح لجدول التقارير عشان تجيب الفروع اللي  تساوي اللي جاي
    print(rolist)
    return JsonResponse( rolist , safe=False)



def view_report(request ):
    #print(request.POST['brand'])
    
    if Term_score.objects.filter( report_order_id = request.POST['orderid']).exists():
        scores = Term_score.objects.filter( report_order_id = request.POST['orderid'])
        print(scores)
        term_result = []
        for score in scores:  
            row = {
                        'description': score.term_id.description,
                        'score' : score.score ,
                        'note': score.note ,
                        'id': score.term_id.id,
                        'img' : str(score.img) ,
                        }
            term_result.append(row)
           

    return JsonResponse( term_result , safe=False)


def get_responisbles(request):
    print(request.POST['termid'])
    responisbles = Term_responsible.objects.filter( term_id = request.POST['termid'])
    res_list =[]
    for responisble in responisbles:     
            row = {
                        'sections': responisble.section_id.description,
                        'name' : responisble.section_id.manager_id.user.first_name + ' ' + responisble.section_id.manager_id.user.last_name ,
                        }
            res_list.append(row)
            print(res_list)
    return JsonResponse( res_list , safe=False)

# فنكشن تعطيها الاوردر اي دي وتعطيك نسبة التقرير
def get_percentage(request):
        scores = Term_score.objects.filter( report_order_id = request.POST['orderid'])
        
        numbers  = []
        for score in scores:    
            print(int(score.score))       
            numbers.append(int(score.score))
        total_sum  = sum(numbers )
        print(total_sum)       
        percentage = (total_sum / len(numbers)) * 100
        print(percentage)  
        data = {
            'percentage':int(percentage),
        }
        return JsonResponse( data , safe=False)






