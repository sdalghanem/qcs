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
    # order id
    terms = Term_score.objects.filter(report_order_id = id)
    data = {
         'username':  request.session['username'] ,
        'img': request.session['img'] ,
        'terms':terms
    }
    return render(request , 'orders/show_order_details.html' ,data)
