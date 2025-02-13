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
from datetime import date
from django.contrib import messages

#عرض الشركات 
def company_list(request):
    if request.user.is_authenticated:
        companies = Company.objects.all()
        data ={
        'username':  request.session['firestName'] ,
        'img': request.session['img'] ,
        'rows': companies ,
         }
        return render(request , 'cloud/company_list.html',data)
    else :
        return render(request , 'inspectors/login.html' )

# اضافة شركة جديدة
def add_new_company(request):
    # if press submit
    if request.user.is_authenticated:
            # recive the value from the form 
            companyName = request.POST['companyName']
            uploaded_file =  request.FILES['companyLogo']
            # check if company name save in db same 
            if Company.objects.filter(description = companyName).exists():
                messages.success(request, "exist")
                return redirect('company_list')
            else:
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name , uploaded_file)
                uploaded_file_url = fs.url(filename)
                newCompany = Company(description = companyName , logo =  uploaded_file_url , registerDate = '2011-11-11')
                newCompany.save()
                messages.success(request, "success")
                # return render(request , 'cloud/add_new_company.html' , {'res' : 'تم حفظ الشركة بنجاح'})
                return redirect('company_list')
    else: 
            return render(request , 'inspectors/login.html')



def brands_dashbord(request, id):    
    if request.user.is_authenticated:
        mngs = Managers.objects.filter(company_id_id = id , position = '1')
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
                                'username':  request.session['firestName'] ,
                                'img': request.session['img']
                                }
                        messages.success(request, "exist")
                        return render(request  , 'cloud/brand_list.html', data)
            else:
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name , uploaded_file)
                uploaded_file_url = fs.url(filename)
                newbrand = Brand(company_id_id = id , description = brandName , logo =  uploaded_file_url , registerDate = '2011-11-11')
                newbrand.save()
                data = {    
                        'mngs' : mngs ,
                        'brands' : brands , 
                        'companyName': companyName ,
                        'companyLogo' : companyLogo ,
                        'res' : 'تم حفظ العلامة التجارية بنجاح',
                        'companyId' : companyId ,
                        'mng_company' : mng_company ,
                        'username':  request.session['firestName'] ,
                        'img': request.session['img']
                              }
            messages.success(request, "success")   
            return render(request , 'cloud/brand_list.html',data)
        else:
            data = {   
                'mngs' : mngs ,
                'brands' : brands ,
                'companyName': companyName ,
                'companyLogo' : companyLogo , 
                'companyId' : companyId , 
                'mng_company' : mng_company ,
                'username':  request.session['firestName'] ,
                'img': request.session['img']
               }
            return render(request , 'cloud/brand_list.html',data)
    else:# if not auth
            return render(request , 'inspectors/login.html')

    #id for company
    # if request.user.is_authenticated:
    #     #مدراء العلامة التجارية
    #     if Managers.objects.filter(company_id_id = id  , position = '1').exists():
    #          mngs = Managers.objects.filter(company_id_id = id , position = '1')
    #     else:
    #         mngs =''
    #     companyName = Company.objects.get(id = id).description
    #     companyLogo = Company.objects.get(id = id).logo
    #     # مدير عام الشركة
    #     if Managers.objects.filter(company_id_id = id  , position = '0').exists():
    #         mng =  Managers.objects.get(company_id_id = id , position = '0')
    #         mng_company = mng.user.first_name + ' ' + mng.user.last_name
    #     else :
    #         mng_company = ''
    #     #print(mng_company)
    #     companyId = id
    #     brands = Brand.objects.filter(company_id_id = id)
    #     data = {
    #         'brands' : brands ,
    #         'companyName': companyName ,
    #         'companyLogo' : companyLogo , 
    #         'companyId' : companyId ,
    #         'mng_company' : mng_company ,
    #         'mngs' : mngs ,
    #         'username':  request.session['firestName'] ,
    #         'img': request.session['img']
    #     }
    #     return render(request , 'cloud/brand_list.html', data)
    # else :
    #     return render(request , 'inspectors/login.html')


def add_new_brand(request , id):
    if request.user.is_authenticated:
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
                                'username':  request.session['firestName'] ,
                                'img': request.session['img']
                                }
                        messages.success(request, "exist")
                        return render(request  , 'cloud/brand_list.html', data)
            else:
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name , uploaded_file)
                uploaded_file_url = fs.url(filename)
                newbrand = Brand(company_id_id = id , description = brandName , logo =  uploaded_file_url , registerDate = '2011-11-11')
                newbrand.save()
                data = {    
                        'mngs' : mngs ,
                        'brands' : brands , 
                        'companyName': companyName ,
                        'companyLogo' : companyLogo ,
                        'res' : 'تم حفظ العلامة التجارية بنجاح',
                        'companyId' : companyId ,
                        'mng_company' : mng_company ,
                        'username':  request.session['firestName'] ,
                        'img': request.session['img']
                              }
            messages.success(request, "success")   
            return render(request , 'cloud/brand_list.html',data)
        else:
            data = {   
                'mngs' : mngs ,
                'brands' : brands ,
                'companyName': companyName ,
                'companyLogo' : companyLogo , 
                'companyId' : companyId , 
                'mng_company' : mng_company ,
                'username':  request.session['firestName'] ,
                'img': request.session['img']
               }
            return render(request , 'cloud/brand_list.html',data)
    else:# if not auth
            return render(request , 'inspectors/login.html')

def regions_city_managers(request , id):
    # id for brand
    # حفظ مدير جديد
    data = {}
    if request.method =='POST':
        print(Brand_regionManager.objects.filter(region_id_id = request.POST['region']  , Brand_id_id = id ).exists())
        if Brand_regionManager.objects.filter(region_id_id = request.POST['region'] , Brand_id_id = id).exists():
            messages.success(request, "error")
            return redirect('regions_city_managers', id = id  )
        elif Brand_regionManager.objects.filter(manager_id_id =request.POST['mngr']).exists():
            messages.success(request, "error")
            return redirect('regions_city_managers', id = id  )

        else:
            
            new = Brand_regionManager()
            new.manager_id_id = request.POST['mngr']
            new.Brand_id_id = request.POST['brandID']
            new.region_id_id = request.POST['region']
            new.registerDate = date.today() 
            new.save()
            messages.success(request, "succcess")

            return redirect('regions_city_managers', id = id )
    else:
    #     # عرض صفحة ادارة المناطق للعلامة التجارية
       
        regMngs = ''
        brand = Brand.objects.get(id= id)
        if Brand_regionManager.objects.filter(Brand_id_id = id).exists:
            regMngs = Brand_regionManager.objects.filter(Brand_id_id = id)
        regions = Region.objects.all()
        mngrs = Managers.objects.filter(company_id_id = brand.company_id.id , position = '2')
        data ={
            'username':  request.session['firestName'] ,
            'img': request.session['img'] ,
            'companyName':   Company.objects.get(id = brand.company_id.id).description,
            'companyLogo' :Company.objects.get(id = brand.company_id.id).logo ,
            'companyID' : brand.company_id.id ,
            'brandName': brand.description ,
            'regMngs' : regMngs ,
            'regions' : regions,
            'mngrs': mngrs,
            'brandID': id ,
           
        }
        return render(request , 'cloud/region_city_mng.html' , data)
    

        
def deleteRegionMngr(request , id):
    # id for brand region manager
    brandID = Brand_regionManager.objects.get(id = id).Brand_id.id
    Brand_regionManager.objects.get(id = id).delete()
    messages.success(request, "delete")
    return redirect('regions_city_managers' , id = brandID )


def cities_managers(request , regionID , brandID):
    # حفظ مدير جديد
    if request.method =='POST':
        if Brand_cityManager.objects.filter(city_id_id = request.POST['city'] , Brand_id_id = request.POST['brandID'] ).exists():
            messages.success(request, "error")
            return redirect('cities_managers', regionID = regionID ,brandID = brandID )
        elif Brand_cityManager.objects.filter( manager_id_id =request.POST['mngr']).exists():
                messages.success(request, "error")
                return redirect('cities_managers', regionID = regionID ,brandID = brandID )
        else:
            new = Brand_cityManager()
            new.manager_id_id = request.POST['mngr']
            new.Brand_id_id = request.POST['brandID']
            new.city_id_id = request.POST['city']
            new.registerDate = date.today() 
            new.save()
            messages.success(request, "succcess")

            return redirect('cities_managers', regionID = regionID ,brandID = brandID )
    # عرض صفحة ادارة المناطق للعلامة التجارية
    cityMngs = []
    brand = Brand.objects.get(id = brandID)
    city = City.objects.filter(region_id = regionID)
    for c in city :
        # if Brand_cityManager.objects.filter(Brand_id_id = brandID , city_id_id = c.id).exists.first():
        #     Mngs = Brand_cityManager.objects.get(Brand_id_id = brandID , city_id_id = c.id)
        #     cityMngs.append(Mngs)
        city_manager = Brand_cityManager.objects.filter(Brand_id_id=brandID, city_id_id=c.id).first()
        if city_manager:
            cityMngs.append(city_manager)
    cities = City.objects.filter( region_id = regionID)

    mngrs = Managers.objects.filter(company_id_id = brand.company_id.id ,position='3' )
    data ={
        'username':  request.session['firestName'] ,
        'img': request.session['img'] ,
        'companyID' : brand.company_id.id ,
        'brandName': brand.description ,
        'cityMngs' : cityMngs ,
        'cities' : cities,
        'mngrs': mngrs,
        'brandID': brandID ,
        'regionID': regionID,
        'companyName':   Company.objects.get(id = brand.company_id.id).description,
        'companyLogo' :Company.objects.get(id = brand.company_id.id).logo ,

    }
    return render(request , 'cloud/cities_mng.html' , data)

def deletecityMngr(request , id , regionID):
    # id for brand region manager
    brandID = Brand_cityManager.objects.get(id = id).Brand_id.id
    Brand_cityManager.objects.get(id = id).delete()
    messages.success(request, "delete")
    return redirect('cities_managers' , brandID = brandID , regionID = regionID) 

def add_new_branch(request , id):
     if request.user.is_authenticated:

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
                        'username':  request.session['firestName'] ,
                        'img': request.session['img']
                        }
                return render(request , 'cloud/brach_list.html',data)
            else:
                newbrand = Branch(brand_id_id = brandId , 
                                description = brachName ,
                                district_id_id = district,
                                registerDate = '2011-11-11')
                newbrand.save()
            
                data = {            'branchs' : branchs ,
                                    'brandName': brandName , 
                                    'brandLogo' : brandLogo ,
                                    'res' : 'تم حفظ الفرع بنجاح', 
                                    'brandId' : brandId ,
                                    'regions' : regions ,
                                    'mngs' : mngs ,
                                    'username':  request.session['firestName'] ,
                                    'img': request.session['img']
                                    }
                return render(request , 'cloud/brach_list.html',data)
        else:
            data = {'branchs' : branchs ,
                    'brandName': brandName ,
                    'brandLogo' : brandLogo ,
                    'brandId' : brandId ,
                    'regions' : regions , 
                    'mngs' : mngs ,
                    'username':  request.session['firestName'] ,
                    'img': request.session['img'],}
            return render(request , 'cloud/brach_list.html', data)
    
     else: # if not auth
        return render(request , 'inspectors/login.html')

def mngrs_data(id):
    row = []
    mngs = Managers.objects.filter(company_id = id)
    for m in mngs :
        if Managers.objects.filter(id = m.id , position = '0').exists():
            d = Managers.objects.get(id = m.id , position = '0')
            row.append({
                'current':  f"مدير {d.company_id.description}" ,
                  'user': m.user,
                  'name' : m.user.first_name + ' ' +m.user.last_name ,
                  'position' : m.position ,
                  'email' :m.user.email ,
                  'mobile': m.mobile,
                  'id': m.id,
                  })
        elif Department.objects.filter(manager_id_id = m.id).exists():
            d = Department.objects.filter(manager_id_id = m.id)
            for t in d :
                row.append({'current': f" مدير ادارة {t.description}" ,
                             'user': m.user,
                            'name' : m.user.first_name + ' ' +m.user.last_name ,
                            'position' : m.position ,
                            'email' :m.user.email ,
                            'mobile': m.mobile,
                              'id': m.id,
                             })
        elif Brand.objects.filter(gm_manager_id_id = m.id).exists():
            d = Brand.objects.get(gm_manager_id_id = m.id)
            row.append({'current':  f" مدير علامة تجارية {d.description}" ,
                        'user': m.user,
                        'name' : m.user.first_name + ' ' +m.user.last_name ,
                        'position' : m.position ,
                        'mobile': m.mobile,
                         'email' :m.user.email ,
                        'id': m.id,
                         })
        elif Section.objects.filter(manager_id_id = m.id).exists():
            d = Section.objects.filter(manager_id_id = m.id)
            for t in d :
                row.append({'current': f" مدير قسم {t.description}" ,
                             'user': m.user,
                            'name' : m.user.first_name + ' ' +m.user.last_name ,
                            'position' : m.position ,
                            'mobile': m.mobile,
                             'email' :m.user.email ,
                            'id': m.id,
                             })
        elif Brand_regionManager.objects.filter(manager_id_id = m.id).exists():
            d= Brand_regionManager.objects.filter(manager_id_id = m.id)
            for t in d :
             row.append({'current': f" مدير منطقة {t.region_id.name}" ,
                        'user': m.user,
                        'name' : m.user.first_name + ' ' +m.user.last_name ,
                        'position' : m.position ,
                        'mobile': m.mobile,
                         'email' :m.user.email ,
                        'id': m.id,
                          })
        elif Brand_cityManager.objects.filter(manager_id_id = m.id).exists():
            d= Brand_cityManager.objects.filter(manager_id_id = m.id)
            for t in d :
                row.append({'current': f" مدير مدينة {t.city_id.name}" , 
                            'user': m.user,
                            'name' : m.user.first_name + ' ' +m.user.last_name ,
                            'position' : m.position ,
                            'mobile': m.mobile,
                             'email' :m.user.email ,
                            'id': m.id,
                            })
        elif Branch.objects.filter(manager_id_id = m.id).exists():
          d= Branch.objects.filter(manager_id_id = m.id)
          for t in d :
                row.append({'current': f" مدير فرع {t.description} {t.brand_id}" , 
                            'user': m.user,
                            'name' : m.user.first_name + ' ' +m.user.last_name ,
                            'position' : m.position ,
                            'mobile': m.mobile,
                             'email' :m.user.email ,
                            'id': m.id,
                            })
        else :
            row.append({'current': "لايوجد منصب حالي" , 
                            'user': m.user,
                            'name' : m.user.first_name + ' ' +m.user.last_name ,
                            'position' : m.position ,
                            'mobile': m.mobile,
                             'email' :m.user.email ,
                            'id': m.id,
                            })

    return row

def users_managment(request , id):
    # id for company
    if request.user.is_authenticated:
      # id  الشركة
        company = Company.objects.get(id = id)
        companyName = company.description
        companyLogo = company.logo

        mngstest = mngrs_data(id) 
        print(mngstest)
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
            'mngs' : mngstest,
            #'mngstest':mngstest,
            'companyName' : companyName,
            'companyLogo' : companyLogo,
            'res':"True",
            'companyID':id,
            'username':  request.session['firestName'] ,
            'img': request.session['img']
            }
            messages.success(request, "succcess_adduser")
            return render(request , 'cloud/users_mng.html' , data)
        else:
            data ={
            'mngs' : mngstest,
            #'mngstest':mngstest,
            'companyName' : companyName,
            'companyLogo' : companyLogo,
            'companyID':id ,
            'username':  request.session['firestName'] ,
            'img': request.session['img']
             }
            return render(request , 'cloud/users_mng.html' , data)
    else: # not auth
        return render(request , 'inspectors/login.html')


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
     userinfo = User.objects.get(id = update.user_id)
     update.position = request.POST['position']
     update.mobile = request.POST['mobile']
     userinfo.email = request.POST['email']
     compid = update.company_id_id
     userinfo.save()
     update.save()
     messages.success(request, "succcess_update")
     return redirect('users_managment' , id = compid) 


def departments(request , id):
    if request.user.is_authenticated:
        #id company
        deptInfo = []
        row = []
        company = Company.objects.get(id = id)
        companyName = company.description
        companyLogo = company.logo
        mngs = Managers.objects.filter(company_id = id , position = '5')
        mngs_sec = Managers.objects.filter(company_id = id , position = '6')
        brands = Brand.objects.filter(company_id = id)
        depts = Department.objects.filter(company_id_id = id)
        for d in depts :
            secInfo = Section.objects.filter(department_id = d.id)
            deptInfo = {
                'deptId' : d.id ,
                'deptName' : d.description ,
                'deptMngr' : d.manager_id ,
                'secifo' : secInfo,
                
            }
            row.append(deptInfo)
        data = {
            'row' : row ,
            'companyName' : companyName,
            'companyLogo' : companyLogo,
            'companyID':id ,
            'mngs' : mngs ,
            'mngs_sec':mngs_sec ,
            'brands' : brands ,
            'username':  request.session['firestName'] ,
            'img': request.session['img']
        }
        return render(request , 'cloud/departments.html' , data)
    else: # not auth 
        return render(request , 'inspectors/login.html')


def add_new_dept(request , id):
    #id company
    description = request.POST['description']
    mngr = request.POST['mngr']
    new_dept = Department()
    new_dept.description = description
    new_dept.manager_id_id = mngr
    new_dept.company_id_id = id
    new_dept.save()
    messages.success(request, "succcess_dept")
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
    messages.success(request, "succcess_sec")
    return redirect('departments' , id = compID) 

def edit_departmentInfo(request , id):
    #id department
    update = Department.objects.get(id = id)
    compID = update.company_id.id
    update.description = request.POST['description']
    update.manager_id_id = request.POST['mngr']
    update.save()
    messages.success(request, "succcess_editdept")
    return redirect('departments' , id = compID)  

def edit_secInfo(request , id):
    #id department
    update = Section.objects.get(id = id)
    compID = update.department_id.company_id.id
    update.description = request.POST['description']
    update.manager_id_id = request.POST['mngr']
    update.save()
    messages.success(request, "succcess_editsec")
    return redirect('departments' , id = compID)



def brand_terms(request , id):
    if request.user.is_authenticated:
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
            'zones': zones ,
            'username':  request.session['firestName'] ,
            'img': request.session['img']
        }
        return render(request , 'cloud/brand_terms.html' , data )
    else: # not auth
        return render(request , 'inspectors/login.html')
