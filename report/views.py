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
    return render(request , 'orders/show_orders.html')

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
    term = Term.objects.get(id = termid)
    if Term_responsible.objects.filter(term_id = term).exists():
        print("موجود")
        update = Term_responsible.objects.get(term_id = term)
        print(update)
        update.section_id_id = request.POST['secid']
        print(update.section_id_id)
        print(request.POST['secid'])
        update.save()
        print("تم الحفظ")
        return redirect('brand_terms' , id = brandid)
    else:
        print("مش موجود")
        new = Term_responsible()
        new.term_id_id = termid
        new.section_id_id = request.POST['secid']
        new.save()
        print("حفظ جديد")
        return redirect('brand_terms' , id = brandid)
    

    


