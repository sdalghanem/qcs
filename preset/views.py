from django.shortcuts import redirect, render
from .models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
# Create your views here.
def packege(request):
    packeges = Packege.objects.all()
    data = { 'row' : packeges}
    return render(request , 'preset/index.html' , data) 

def add_new_packages(request):
    if  Packege.objects.filter(description = request.POST['brandName']).exists(): 
        packeges = Packege.objects.all()
        data = {
                'row' : packeges ,
                "msg": 'اسم الباقة موجود مسبقاً' ,
                'class' :'alert-warning'
                }
        return render(request , 'preset/index.html' , data ) 
    else :
        brandName = request.POST['brandName']
        newPck = Packege()
        newPck.description = brandName
        newPck.save()
        packeges = Packege.objects.all()
        data = {
                'row' : packeges ,
                "msg": 'تم الحفظ بنجاح' ,
                'class' :'alert-success'
                }
        return render(request , 'preset/index.html' , data) 

# تفاصيل الباقة
def packege_details(request , id):
    #id packege
    print(id)
    pck =Packege.objects.get(id = id)
    titles = Term_title.objects.filter(packege_id = id)
    data = {
        'pckName' : pck.description ,
        'pkid': id ,
        'titles': titles
    }
    return render(request , 'preset/packages_details.html' , data) 

# صفحة اضافة تفاصيل تصنيف جديد
def add_termsPage(request , id):
    title = Term_title.objects.get(id = id)
    data = {
        'titleID' : id ,
        'pkid' : title.packege_id_id,
    }
    return render(request , 'preset/new_terms.html' , data) 


# صفحة اضافة تفاصيل تصنيف جديد
def add_new_terms(request):
    terms = json.loads(request.POST['terms'])
    titleID = request.POST['titleID']
    for t in terms:
        new = Preset_terms()
        new.description = t
        new.term_title_id_id = titleID
        new.save()
    
    data = {
        'terms' : 'ok',
       # 'sec': request.POST['secName']
    }
    return JsonResponse( data , safe=False)



# تفاصيل التصنيف
def section_details(request , id ):
    #id title
    title =Term_title.objects.get(id = id).section
    terms = Preset_terms.objects.filter(term_title_id = id)
    data = {
        'title' : title ,
        'terms': terms,
    }
    return render(request , 'preset/section_details.html' , data) 

def add_new_term_title(request , id):
    #id pagege
    newTitle = Term_title()
    newTitle.section = request.POST['description']
    newTitle.packege_id_id = id
    newTitle.save()
    return redirect('packege_details' , id = id)

def update_term_title(request , id):
    #id title
    update = Term_title.objects.get(id = id)
    pkid = update.packege_id_id
    update.section = request.POST['description']
    update.save()
    return redirect('packege_details' , id = pkid)
    pass

def delete_term(request , id):
    term = Preset_terms.objects.get(id = id)
    titid = term.term_title_id.id
    term.delete()
    return redirect(section_details , id = titid)