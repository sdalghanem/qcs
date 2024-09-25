from django.shortcuts import redirect, render
from .models import *
from cloudteam.views import *
from preset.models import *
from report.models import *
# Create your views here.
def get_dept_score_by_secID(id):
    respons = Term_responsible.objects.get(section_id = id)
    term = Term_score.objects.get(term_id = respons.term_id)
    print(term)
    return term

def show_orders(request):
    orders = Report_order.objects.all()
    data = {
        'orders' : orders
    }
    return render(request , 'orders/show_orders.html' , data)

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
            'brandId' : term.brand_id.id}
    return render(request , 'orders/show_termsResponsibles.html' , data)


def delete_responsible(request , id):
    #id term responsible
    term = Term_responsible.objects.get(id = id)
    term.delete()
    return redirect('show_responsible' , id = term.term_id.id )



