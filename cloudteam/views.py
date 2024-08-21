from django.shortcuts import render
from clients.models import * 
# اضافه بروفايل شركة
# اضافة براند
from django.core.files.storage import FileSystemStorage



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

def add_new_brand(request , id):
     # id  الشركة
     companyName = Company.objects.get(id = id).description
     companyLogo = Company.objects.get(id = id).logo
     mng_company =  Managers.objects.get(company_id_id = id , gm_manager = 1 ).user
     print(mng_company)
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
                              }
                    return render(request  , 'cloud/brand_list.html', data)
        else:
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name , uploaded_file)
            uploaded_file_url = fs.url(filename)
            newbrand = Brand(company_id_id = id , description = brandName , logo =  uploaded_file_url , registerDate = '2011-11-11')
            newbrand.save()
           
        return render(request , 'cloud/brand_list.html',{'brands' : brands , 'companyName': companyName , 'companyLogo' : companyLogo ,'res' : 'تم حفظ العلامة التجارية بنجاح', 'companyId' : companyId , 'mng_company' : mng_company ,})
     else:
        return render(request , 'cloud/brand_list.html',{'brands' : brands ,'companyName': companyName , 'companyLogo' : companyLogo , 'companyId' : companyId , 'mng_company' : mng_company ,})
     
def add_new_branch(request , id):
     # id  العلامة التجارية
     brandName = Brand.objects.get(id = id).description
     brandLogo = Brand.objects.get(id = id).logo
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
                            'regions' : regions}
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
                                'regions' : regions}
            return render(request , 'cloud/brach_list.html',data)
     else:
        data = {'branchs' : branchs ,
                'brandName': brandName ,
                'brandLogo' : brandLogo ,
                'brandId' : brandId ,
                'regions' : regions}
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
            newMng.gm_manager = 0
            newMng.task_traker = 0
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
   

        
      