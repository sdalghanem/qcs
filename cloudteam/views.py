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

#عرض الشركات 
def company_list(request):
    companies = Company.objects.all()
    return render(request , 'cloud/company_list.html',{'rows': companies})

# اضافة شركة جديدة
def add_new_company(request):
    # if press submit
    if request.method =='POST':
        # recive the value from the form 
        companyName = request.POST['companyName']
        uploaded_file =  request.FILES['companyLogo']
        # check if company name save in db same 
        if Company.objects.filter(description = companyName).exists():
            return render(request , 'cloud/add_new_company.html' , {'res' : 'اسم الشركة مسجل مسبقاَ'})
        else:
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name , uploaded_file)
            uploaded_file_url = fs.url(filename)
            newCompany = Company(description = companyName , logo =  uploaded_file_url , registerDate = '2011-11-11')
            newCompany.save()
            return render(request , 'cloud/add_new_company.html' , {'res' : 'تم حفظ الشركة بنجاح'})

    else:
        return render(request , 'cloud/add_new_company.html')


def brands_dashbord(request, id):
     mngs = Managers.objects.filter(company_id_id = id)
     companyName = Company.objects.get(id = id).description
     companyLogo = Company.objects.get(id = id).logo
     if Managers.objects.filter(company_id_id = id  , position = '0').exists():
        mng =  Managers.objects.get(company_id_id = id , position = '0')
        mng_company = mng.user
     else :
        mng_company = ''
     #print(mng_company)
     companyId = id
     brands = Brand.objects.filter(company_id_id = id)
     data = {
          'brands' : brands ,
          'companyName': companyName ,
          'companyLogo' : companyLogo , 
          'companyId' : companyId ,
          'mng_company' : mng_company ,
          'mngs' : mngs ,
     }
     return render(request , 'cloud/brand_list.html', data)

def add_new_brand(request , id):
     mngs = Managers.objects.filter(company_id_id = id)
     # id  الشركة
     companyName = Company.objects.get(id = id).description
     companyLogo = Company.objects.get(id = id).logo
     if Managers.objects.filter(company_id_id = id  , position = '0').exists():
        mng =  Managers.objects.get(company_id_id = id , position = '0')
        mng_company = mng.user
     else :
        mng_company = ''     
     companyId = id
     brands = Brand.objects.filter(company_id_id = id)
     if request.method =='POST':
        brandName = request.POST['brandName']
        uploaded_file =  request.FILES['brandLogo']
        # check if company name save in db same 
        if Brand.objects.filter(description = brandName).exists():
                    data = {'brands' : brands ,
                            'companyName': companyName ,
                              'companyLogo' : companyLogo ,
                              'res' : 'موجود مسبقاً', 
                              'companyId' : companyId , 
                              'mng_company' : mng_company , 
                              'mngs' : mngs ,
                              }
                    return render(request  , 'cloud/brand_list.html', data)
        else:
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name , uploaded_file)
            uploaded_file_url = fs.url(filename)
            newbrand = Brand(company_id_id = id , description = brandName , logo =  uploaded_file_url , registerDate = '2011-11-11')
            newbrand.save()
           
        return render(request , 'cloud/brand_list.html',{   'mngs' : mngs ,'brands' : brands , 'companyName': companyName , 'companyLogo' : companyLogo ,'res' : 'تم حفظ العلامة التجارية بنجاح', 'companyId' : companyId , 'mng_company' : mng_company ,})
     else:
        return render(request , 'cloud/brand_list.html',{   'mngs' : mngs ,'brands' : brands ,'companyName': companyName , 'companyLogo' : companyLogo , 'companyId' : companyId , 'mng_company' : mng_company ,})
     
def add_new_branch(request , id):
     brand = Brand.objects.get(id = id)
     mngs = Managers.objects.filter( company_id = brand.company_id)
     # id  العلامة التجارية
     brandName = brand.description
     brandLogo = brand.logo
     brandId = id
     branchs = Branch.objects.filter(brand_id_id = id)
     regions = Region.objects.filter(country_id = 1)
     if request.method =='POST':
        brachName = request.POST['brachName']
        district = request.POST['district']
        # check if company name save in db same 
        if Branch.objects.filter(description = brachName).exists():
            data = {'branchs' : branchs ,
                    'brandName': brandName , 
                    'brandLogo' : brandLogo ,
                    'res' : 'موجود مسبقاً', 
                    'brandId' : brandId,
                    'regions' : regions ,
                    'mngs' : mngs ,
                    }
            return render(request , 'cloud/brach_list.html',data)
        else:
            newbrand = Branch(brand_id_id = brandId , 
                              description = brachName ,
                              district_id_id = district,
                              registerDate = '2011-11-11')
            newbrand.save()
           
            data = {'branchs' : branchs ,
                                'brandName': brandName , 
                                'brandLogo' : brandLogo ,
                                'res' : 'تم حفظ الفرع بنجاح', 
                                'brandId' : brandId ,
                                'regions' : regions ,
                                'mngs' : mngs ,}
            return render(request , 'cloud/brach_list.html',data)
     else:
        data = {'branchs' : branchs ,
                'brandName': brandName ,
                'brandLogo' : brandLogo ,
                'brandId' : brandId ,
                'regions' : regions , 
                'mngs' : mngs ,}
        return render(request , 'cloud/brach_list.html', data)

def users_managment(request , id):
      # id  الشركة
        company = Company.objects.get(id = id)
        companyName = company.description
        companyLogo = company.logo
        mngs = Managers.objects.filter(company_id = id)
        if  request.method =='POST':
            newUser = User()
            newUser.username = request.POST['username']
            newUser.first_name = request.POST['first_name']
            newUser.last_name = request.POST['last_name']
            newUser.email = request.POST['email']
            newUser.set_password(request.POST['password'])
            newUser.save()

            newMng = Managers()
            newMng.user_id = newUser.id 
            newMng.company_id = company
            newMng.mobile = request.POST['mobile']
            #newMng.gm_manager = 0
            #newMng.task_traker = 0
            newMng.position = request.POST['position']
            newMng.save()
            data ={
            'mngs' : mngs,
            'companyName' : companyName,
            'companyLogo' : companyLogo,
            'res':"تم حفظ المستخدم بنجاح",
            'companyID':id
            }
            return render(request , 'cloud/users_mng.html' , data)
        else:
            data ={
            'mngs' : mngs,
            'companyName' : companyName,
            'companyLogo' : companyLogo,
            'companyID':id
             }
            return render(request , 'cloud/users_mng.html' , data)
   

 # تحديث مدير علامة تجارية       
def update_company_mngs(request , id):
     update = Brand.objects.get(id = id)
     compid = update.company_id_id
     update.gm_manager_id_id = request.POST['mngr']
     update.save()
     return redirect('brands_dashbord' , id = compid) 

 # تحديث مدير فرع       
def update_branch_mngs(request , id):
     update = Branch.objects.get(id = id)
     brandid = update.brand_id_id
     update.manager_id_id = request.POST['mngr']
     update.save()
     return redirect('add_new_branch' , id = brandid) 

 # تحديث منصب المدير       
def update_position_mngs(request , id):
     #id manager
     update = Managers.objects.get(id = id)
     update.position = request.POST['position']
     compid = update.company_id_id
     update.save()
     return redirect('users_managment' , id = compid) 


def departments(request , id):
    #id company
    deptInfo = []
    row = []
    company = Company.objects.get(id = id)
    companyName = company.description
    companyLogo = company.logo
    mngs = Managers.objects.filter(company_id = id)
    brands = Brand.objects.filter(company_id = id)
    depts = Department.objects.filter(company_id_id = id)
    for d in depts :
         secInfo = Section.objects.filter(department_id = d.id)
         deptInfo = {
             'deptId' : d.id ,
              'deptName' : d.description ,
              'deptMngr' : d.manager_id ,
              'secifo' : secInfo
         }
         row.append(deptInfo)
    data = {
       'row' : row ,
        'companyName' : companyName,
        'companyLogo' : companyLogo,
        'companyID':id ,
        'mngs' : mngs ,
        'brands' : brands ,
    }
    return render(request , 'cloud/departments.html' , data)

def add_new_dept(request , id):
    #id company
    description = request.POST['description']
    mngr = request.POST['mngr']
    new_dept = Department()
    new_dept.description = description
    new_dept.manager_id_id = mngr
    new_dept.company_id_id = id
    new_dept.save()
    return redirect('departments' , id = id) 

def add_new_sec(request , id):
    #id department
    compID = Department.objects.get(id = id).company_id.id
    description = request.POST['description']
    mngr = request.POST['mngr']
    brand = request.POST['brand']
    new_sec = Section()
    new_sec.description = description
    new_sec.Brand_id_id = brand
    new_sec.manager_id_id = mngr
    new_sec.department_id_id = id
    new_sec.save()
    return redirect('departments' , id = compID) 

def edit_departmentInfo(request , id):
    #id department
    update = Department.objects.get(id = id)
    compID = update.company_id.id
    update.description = request.POST['description']
    update.manager_id_id = request.POST['mngr']
    update.save()
    return redirect('departments' , id = compID)  

def edit_secInfo(request , id):
    #id department
    update = Section.objects.get(id = id)
    compID = update.department_id.company_id.id
    update.description = request.POST['description']
    update.manager_id_id = request.POST['mngr']
    update.save()
    return redirect('departments' , id = compID)



def brand_terms(request , id):
    #id for brand
    brandName = Brand.objects.get(id = id)
    zones = Zone.objects.filter(brand_id = id)
    company = Company.objects.get(id = brandName.company_id.id)
    pcks = Packege.objects.all()
    secs = Section.objects.filter(Brand_id = id)
    print(company.packege)
    if  company.packege :
        #print(packege_terms(company.packege.id))
       # terms = packege_terms(company.packege.id)
       terms = Term.objects.filter(brand_id = id , cancel = 0)
    else:
        terms = ''
        
    data ={
        'brandName' : brandName ,
        'pcks' : pcks ,
        'brandId': id ,
        'pckName' : company.packege,
        'terms' : terms ,
        'secs' : secs ,
        'companyId' :company.id ,
        'zones': zones
    }
    return render(request , 'cloud/brand_terms.html' , data )

#API
def save_packege(request):
    # اضافه البنود بناء على تفعيل الباقة للشركة
    # اذا كان البند موجود فقط نقول بتحويل الكنسل الى 0
    # اذا كان البند غير موجود نقول بحفظه
    # اذا كان البند الموجود من غير الباقه المفعله نقوم بتحويل الكنسل الى 1

    pck = request.POST['pck']
    brandId = request.POST['brandId']
    brand = Brand.objects.get(id = brandId)
    update = Company.objects.get(id = brand.company_id.id)
    
    update.packege_id = pck
    update.save()
    #print(packege_terms(update.packege.id))
    # حفظ البنود بناء على الباقة
    preset = packege_terms(update.packege.id)
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





#######################################inspectors#########################################

def show_inspectors(request):
    emps = Employee.objects.all()
    data ={
        'emps': emps,
        'username':  request.session['username'] ,
        'img': request.session['img']
    }
    return render(request , 'inspectors/show_inspectors.html' , data)

def new_inspectors_form(request):
    if  request.method =='POST':
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
            #
            uploaded_file =  request.FILES['profile_img']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name , uploaded_file)
            uploaded_file_url = fs.url(filename)
            #
            newEmp.profile_img = uploaded_file_url
            newEmp.save()
            data ={
                'res' : 'تم حفظ الموظف بنجاح'
            }
            return render(request , 'inspectors/addNewInspectors.html' , data)
    return render(request , 'inspectors/addNewInspectors.html')


def edit_Inspectors(request , id):
        #id for employee
        emp = Employee.objects.get(id = id)
        user = User.objects.get(id = emp.user.id)
        data ={
            'userinfo' :  user ,
            'empinfo': emp ,
        }
        if  request.method =='POST':
            email = request.POST['email']
            mobile = request.POST['mobile']
            psw= request.POST['password']
            updatEmp = Employee.objects.get(id = id)
            updateUser = User.objects.get(id = updatEmp.user.id)
            updatEmp.mobile = mobile
            updateUser.email = email
            updateUser.set_password(psw)
            updateUser.save()
            updatEmp.save()
            return redirect('/cloudteam/show_inspectors')
        return render(request , 'inspectors/editInspectors.html' , data)

def login_admin(request):
    if  request.method =='POST':
                mngUsername = request.POST['username']
                mngPassword = request.POST['password']
                result = authenticate(username = mngUsername , password = mngPassword)
                print(result)
                if result is not None:
                    auth_login(request, result) 
                    userInfo = User.objects.get(username = mngUsername)
                    emp = Employee.objects.get(user_id = userInfo.id)
                    # save data on session
                    request.session['id'] = userInfo.id
                    request.session['firestName'] = userInfo.first_name
                    request.session['lastName'] = userInfo.last_name   
                    request.session['username'] = userInfo.username
                    request.session['img'] = str(emp.profile_img)
                    return redirect('/cloudteam/show_inspectors')
                else :
                     return render(request , 'inspectors/login.html' , {'res' : 'كلمة المرور او اسم المستخدم غير صحيح'})
                     
    return render(request , 'inspectors/login.html')
