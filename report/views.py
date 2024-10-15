from django.shortcuts import redirect, render
from .models import *
from cloudteam.views import *
from preset.models import *
from report.models import *
from datetime import date
# Create your views here.
def get_dept_score_by_secID(id):
    respons = Term_responsible.objects.get(section_id = id)
    term = Term_score.objects.get(term_id = respons.term_id)
    print(term)
    return term

def show_orders(request):
    if request.user.is_authenticated:
        orders = Report_order.objects.all()
        data = {
            'orders' : orders ,
            'username':  request.session['username'] ,
            'img': request.session['img']
        }
        return render(request , 'orders/show_orders.html' , data)
    else:
         return render(request , 'inspectors/login.html')

def new_order(request):
    if request.user.is_authenticated:

        if request.method =='POST':
            new = Report_order()
            new.bransh_id_id = request.POST['branch']
            new.employee_id_id = request.POST['employee']
            new.registerDate = date.today()
            new.year = request.POST['year']
            new.quarter = request.POST['quarter']
            new.save()
            return redirect('show_orders')
        comppanies = Company.objects.all()
        emps = Employee.objects.filter(supervisor = 0 , manager=0)
        data = {
            'comppanies' : comppanies ,
            'emps' : emps ,
            'username':  request.session['username'] ,
            'img': request.session['img']
        }
        return render(request , 'orders/new_order.html' , data)
    else: # not auth
        return render(request , 'inspectors/login.html')


#########API #############
def get_brand(request):
    comp_id = request.POST['company_id']
    brands = Brand.objects.filter(company_id = comp_id)
    row = []
    for b in brands :
        row.append({'name': b.description , 'id': b.id})
    return JsonResponse( row , safe=False)

def get_branch(request):
    brand_id = request.POST['brand_id']
    branchs = Branch.objects.filter(brand_id = brand_id)
    row = []
    for b in branchs :
        row.append({'name': b.description , 'id': b.id})
    return JsonResponse( row , safe=False)
########zone ####################

def add_newZone(request , id):
# id for brand 
    new = Zone()
    new.name = request.POST['name']
    new.brand_id_id = id
    new.save()
    return redirect('brand_terms' , id = id)


def insert_responsible(request , brandid , termid):
    #id for term
    # term = Term.objects.get(id = termid)
    new = Term_responsible()
    new.term_id_id = termid
    new.section_id_id = request.POST['secid']
    new.zone_id_id = request.POST['zoneid']
    new.save()
    print("حفظ جديد")
    return redirect('brand_terms' , id = brandid)
    

    
def show_responsible(request,id):
    if request.user.is_authenticated:
        #id for term
        row = []
        term = Term.objects.get(id = id)
        print(term.description)
        respons = Term_responsible.objects.filter(term_id_id = id)
        for r in respons:
            row.append({'secName' : r.section_id.description,
                        'zoneName' : r.zone_id.name,
                        'resId' : r.id,
                        })
        data = {'term_desc' : term.description,
                'respons' : row ,
                'brandId' : term.brand_id.id ,
                'username':  request.session['username'] ,
                'img': request.session['img']
        }
        return render(request , 'orders/show_termsResponsibles.html' , data)
    else:
        return render(request , 'inspectors/login.html')


def delete_responsible(request , id):
    #id term responsible
    term = Term_responsible.objects.get(id = id)
    term.delete()
    return redirect('show_responsible' , id = term.term_id.id )



def show_order_details(request , id):
    # id -> order id
    if request.user.is_authenticated:
        if  Term_score.objects.filter(report_order_id_id = id).exists:
                terms = Term_score.objects.filter(report_order_id_id = id)
                orinfo = Report_order.objects.filter(id = id) # استخدمنا فلتر عشان تاخذ كل البيانات
                if Score_history.objects.filter(report_order_id_id = id).exists():
                    btnOn = '0'
                else:
                    btnOn = '1'
                data = {
                    'username':  request.session['username'] ,
                    'img': request.session['img'] ,
                    'terms':terms , # البنود المقيمة
                    'orinfo': orinfo , # معلومات الطلب
                    'fainl_res': calc_order(id) ,# النتيجه النهائية
                     'btnOn' : btnOn , # اظهار زر الاعتماد
                }
                return render(request , 'orders/show_order_details.html' ,data)
        else:
              data = {
                    'username':  request.session['username'] ,
                    'img': request.session['img'] ,
              }
              return render(request , 'orders/show_order_details.html' ,data)
    else:
        return render(request , 'inspectors/login.html')


def calc_order(id):
    #id for order
      # جلب جميع السجلات المرتبطة بالطلب المحدد
    scores = Term_score.objects.filter(report_order_id_id=id)

    # التحقق من وجود درجات
    if not scores.exists():
        return 0  # إذا لم تكن هناك درجات، أعد 0

    # حساب مجموع الدرجات (والتي هي إما 0 أو 1)
    total_score = sum(int(score.score) for score in scores)

    # حساب عدد البنود (terms) وهو العدد الكلي للدرجات الممكنة
    total_terms = scores.count()

    # حساب النسبة المئوية وتحويلها إلى عدد صحيح
    percentage = int((total_score / total_terms) * 100) if total_terms > 0 else 0

    return percentage


def submit_result(request , resault , orderid):
    ord = Report_order.objects.get(id=orderid)
    new = Score_history()
    new.report_order_id_id = orderid
    new.total_score = resault
    new.quarter = ord.quarter
    new.year = ord.year
    new.registerDate = date.today()
    new.save()
    return redirect('show_order_details' , id=orderid)
    