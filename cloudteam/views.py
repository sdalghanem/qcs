from django.shortcuts import redirect, render
from clients.models import * 
# اضافه بروفايل شركة
# اضافة براند
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from preset.models import *
from report.models import *
import json
from django.contrib.auth import authenticate , login as auth_login , logout
from django.contrib import messages

#API
def save_packege(request):
    # اضافه البنود بناء على تفعيل الباقة للشركة
    # اذا كان البند موجود فقط نقول بتحويل الكنسل الى 0
    # اذا كان البند غير موجود نقوم بحفظه
    # اذا كان البند الموجود من غير الباقه المفعله نقوم بتحويل الكنسل الى 1

    pck = request.POST['pck']
    brandId = request.POST['brandId']
    brand = Brand.objects.get(id = brandId)
    #update = Company.objects.get(id = brand.company_id.id)
    
    brand.packege_id = pck
    brand.save()
    #print(packege_terms(update.packege.id))
    # حفظ البنود بناء على الباقة
    preset = packege_terms(brand.packege.id)
    # تحول جميع البنود الى ملغيه 
    if Term.objects.filter(brand_id_id = brandId).exists:
        cancel = Term.objects.filter(brand_id_id = brandId)
        for c in cancel:
            c.cancel = 1
            c.save()
    for p in preset :
        for t in p['terms']:
            new = Term()
            new.description = t['term']
            new.brand_id_id =brandId
            new.cancel = 0
            new.save()
            #print(t['term'])
    return JsonResponse( {'data' : 'ok'} , safe=False)
  
def packege_terms(id):
    #id for pck
    allterm = []
    title = Term_title.objects.filter(packege_id_id = id)
    for tit in title :
        row = []
        pres = Preset_terms.objects.filter(term_title_id_id = tit.id)
        for p in pres:
            row.append({ 'term' : p.description , 'id': p.id})
        allterm.append({'title' : tit.section , 'terms': row}) 
    return allterm

def remove_note(request):
     update = Term.objects.get(id = request.POST['termid'])
     update.note = ''
     update.save()
     return JsonResponse( {'data' : 'ok'} , safe=False)



#######################################inspectors#########################################

def show_inspectors(request):
    emps = Employee.objects.filter(manager = 0 , supervisor = 0)
    data ={
        'emps': emps,
        'username':  request.session['username'] ,
        'img': request.session['img']
    }
    return render(request , 'inspectors/show_inspectors.html' , data)

def new_inspectors_form(request):
    if request.method == 'POST':
        # التحقق من وجود اسم المستخدم مسبقاً
        if User.objects.filter(username=request.POST['username']).exists():
            messages.success(request, "exist")
            return redirect('new_inspectors_form')
        else:
            newUser = User()
            newUser.username = request.POST['username']
            newUser.first_name = request.POST['first_name']
            newUser.last_name = request.POST['last_name']
            newUser.email = request.POST['email']
            newUser.set_password(request.POST['password'])
            newUser.save()

            newEmp = Employee()
            newEmp.user_id = newUser.id 
            newEmp.mobile = request.POST['mobile']
            newEmp.supervisor = 0
            newEmp.manager = 0
            
            # حفظ الصورة المرفوعة
            uploaded_file = request.FILES['profile_img']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(filename)
            
            newEmp.profile_img = uploaded_file_url
            newEmp.save()

            messages.success(request, "success_newuser")
            return redirect('show_inspectors')

    return render(request, 'inspectors/addNewInspectors.html', {
        'username': request.session['username'],
        'img': request.session['img']
    })



from django.core.files.storage import FileSystemStorage

def edit_Inspectors(request, id):
    if request.user.is_authenticated:
        # استرجاع بيانات الموظف والمستخدم
        emp = Employee.objects.get(id=id)
        user = User.objects.get(id=emp.user.id)
        data = {
            'userinfo': user,
            'empinfo': emp,
            'username': request.session['username'],
            'img': request.session['img']
        }
        if request.method == 'POST':
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            psw = request.POST.get('password', '').strip()  # الحصول على قيمة كلمة المرور إن وُجدت

            updatEmp = Employee.objects.get(id=id)
            updateUser = User.objects.get(id=updatEmp.user.id)
            # تحديث البريد الإلكتروني ورقم الجوال
            updateUser.email = email
            updatEmp.mobile = mobile

            # تغيير كلمة المرور فقط إذا كانت القيمة غير فارغة
            if psw:
                updateUser.set_password(psw)
            
            # تعديل صورة البروفايل إذا تم رفع ملف جديد
            if 'profile_img' in request.FILES:
                uploaded_file = request.FILES['profile_img']
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                uploaded_file_url = fs.url(filename)
                updatEmp.profile_img = uploaded_file_url

            updateUser.save()
            updatEmp.save()
            messages.success(request, "edit")
            return redirect('/cloudteam/show_inspectors')

            
        return render(request, 'inspectors/editInspectors.html', data)
    else:
        return render(request, 'inspectors/login.html')




def login_admin(request):
    if  request.method =='POST':
                mngUsername = request.POST['username']
                mngPassword = request.POST['password']
                result = authenticate(username = mngUsername , password = mngPassword)
                print(result)
                if result is not None:
                    userInfo = User.objects.get(username = mngUsername)
                    if Employee.objects.filter(user_id = userInfo.id , supervisor = '1').exists():
                        emp = Employee.objects.get(user_id = userInfo.id , supervisor = '1')
                        auth_login(request, result) 
                        # save data on session
                        request.session['id'] = userInfo.id
                        request.session['firestName'] = userInfo.first_name
                        request.session['lastName'] = userInfo.last_name   
                        request.session['username'] = userInfo.username
                        request.session['img'] = str(emp.profile_img)
                        return redirect('/cloudteam/company_list')
                    else:
                        return render(request , 'inspectors/login.html' , {'res' : 'ليس لديك صلاحية'})

                else :
                     return render(request , 'inspectors/login.html' , {'res' : 'كلمة المرور او اسم المستخدم غير صحيح'})
                     
    return render(request , 'inspectors/login.html')

def logout_view(request):
    logout(request)
    return redirect('login_admin')  # Redirect to login page after logging out
