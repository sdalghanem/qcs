from django.shortcuts import redirect, render
from .models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
# Create your views here.
def packege(request):
    if request.user.is_authenticated:
        packeges = Packege.objects.all()
        data = { 'row' : packeges,
                'username':  request.session['username'] ,
                'img': request.session['img'],
                }
        return render(request , 'preset/index.html' , data) 
    else:
        return render(request , 'inspectors/login.html')


def add_new_packages(request):
    if request.user.is_authenticated:
        if  Packege.objects.filter(description = request.POST['brandName']).exists(): 
            packeges = Packege.objects.all()
            
            data = {
                    'row' : packeges ,
                    "msg": 'اسم الباقة موجود مسبقاً' ,
                    'class' :'alert-warning' ,
                    'username':  request.session['username'] ,
                    'img': request.session['img']
                    }
            return render(request , 'preset/index.html' , data ) 
        else :
            brandName = request.POST['brandName']
            newPck = Packege()
            newPck.description = brandName
            newPck.save()
            print('هذا الاي دي الجديد')
            print(newPck.id)
            return redirect('packege_details' , id = newPck.id)
            #
            # data = {
            #         'row' : packeges ,
            #         "msg": 'تم الحفظ بنجاح' ,
            #         'class' :'alert-success' ,
            #         'username':  request.session['username'] ,
            #         'img': request.session['img']
            #         }
            #return render(request , 'preset/index.html' , data) 

    else :
            return render(request , 'inspectors/login.html')


# تفاصيل الباقة
def packege_details(request , id):
    if request.user.is_authenticated:
        row=[]
        #id packege
        print(id)
        pck =Packege.objects.get(id = id)
        titles = Term_title.objects.filter(packege_id = id)
        # استخراج جميع البنود التابعه للعنوان
        for t in titles :
            if Preset_terms.objects.filter(term_title_id = t.id).exists:
                pre = Preset_terms.objects.filter(term_title_id = t.id)
                row.append({'title_id': t.id ,'title': t.section , 'terms': pre})
        data = {
            'pckName' : pck.description ,
            'pkid': id ,
            'titles': titles ,
            'username':  request.session['username'] ,
            'img': request.session['img'],
            'row': row,
        }
        return render(request , 'preset/packages_details.html' , data) 
    else :
        return render(request , 'inspectors/login.html')


# صفحة اضافة تفاصيل تصنيف جديد
def add_termsPage(request , id):
    if request.user.is_authenticated:
        title = Term_title.objects.get(id = id)
        data = {
            'titleID' : id ,
            'pkid' : title.packege_id_id,
            'pckName' : title.packege_id.description,
            'title': title.section,
            'username':  request.session['username'] ,
            'img': request.session['img']
        }
        return render(request , 'preset/new_terms.html' , data) 
    else :
        return render(request , 'inspectors/login.html')



# صفحة اضافة تفاصيل تصنيف جديد
def add_new_terms(request):
    if request.user.is_authenticated:
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
    else :
        return render(request , 'inspectors/login.html')




# تفاصيل التصنيف
def section_details(request , id ):
    if request.user.is_authenticated:
        #id title
        title = Term_title.objects.get(id = id).section
        terms = Preset_terms.objects.filter(term_title_id = id)
        data = {
            'title' : title ,
            'terms': terms,
            'pckName': Term_title.objects.get(id = id).packege_id.description,
            'pckid': Term_title.objects.get(id = id).packege_id.id,
            'username':  request.session['username'] ,
            'img': request.session['img']
        }
        return render(request , 'preset/section_details.html' , data) 
    else:
        return render(request , 'inspectors/login.html')


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
    

def delete_term(request , id):
    term = Preset_terms.objects.get(id = id)
    packid = term.term_title_id.packege_id.id
    term.delete()
    return redirect('packege_details' , id = packid)

def delete_package(request , id):
    # id for package
    pck = Packege.objects.get(id = id)
    if Term_title.objects.filter(packege_id = id).exists():
        return redirect(packege)
    else :
        pck.delete()
        return redirect(packege)
    
def edit_pck_title(request , id) :
        pck = Packege.objects.get(id = id)
        pck.description = request.POST['description']
        pck.save()
        return redirect(packege)
