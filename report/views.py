from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from cloudteam.views import *
from preset.models import *
from report.models import *
from clients.models import *
from datetime import date
from django.contrib import messages
import datetime
from django.http import JsonResponse

# Create your views here.
def get_dept_score_by_secID(id):
    respons = Term_responsible.objects.get(section_id = id)
    term = Term_score.objects.get(term_id = respons.term_id)
    print(term)
    return term

# def remove_order(request):
#     ids = request.POST.getlist('selectedIds[]')
#     for id in ids:
#         if Report_order.objects.filter(id = id , status = '0').exists():
#             Report_order.objects.get(id = id).delete()
#             return True
        
#     return JsonResponse(ids, safe=False)



def remove_order(request):
    if request.method != "POST":
        return JsonResponse("erorr", safe=False, status=405)
    
    ids = request.POST.getlist('selectedIds[]')
    total_ids = len(ids)
    deleted_count = 0

    for order_id in ids:
        try:
            # نحاول الحصول على الطلب الذي حالته '0'
            order = Report_order.objects.get(id=order_id, status='0')
            order.delete()
            deleted_count += 1
        except Report_order.DoesNotExist:
            # إذا لم يكن الطلب موجودًا أو لا تطابق الحالة المطلوبة، نتجاهله
            continue

    # إذا لم يتم إرسال أية IDs أو لم يتم حذف أي منها
    if total_ids == 0 or deleted_count == 0:
        return JsonResponse("error", safe=False)
    # إذا تم حذف جميع الـ IDs
    elif deleted_count == total_ids:
        return JsonResponse("ok", safe=False)
    # إذا تم حذف بعضها فقط
    else:
        return JsonResponse("notall", safe=False)


def show_orders(request , id):
    #id for brand
    if request.user.is_authenticated:
        orders = []
        Branchs = Branch.objects.filter(brand_id = id)
        for b in Branchs :
            order = Report_order.objects.filter(bransh_id = b.id )
            for o in order:
                orders.append({
                    'id' : o.id ,
                    'bransh_id' : b.id ,
                    'branchName': b.description ,
                    'status' : o.status ,
                    'quarter': o.quarter ,
                    'year' : o.year ,
                    'employee_id' : o.employee_id ,
                    'registerDate': o.registerDate ,
                })
        data = {
            'orders' : orders ,
            'brand_id' : id ,
            'brandLogo' : Brand.objects.get(id = id).logo ,
            'brandName' : Brand.objects.get(id = id).description ,
            'companyId': Brand.objects.get(id = id).company_id.id ,
            'username':  request.session['username'] ,
            'img': request.session['img'],
            'emps':  Employee.objects.filter(supervisor = 0 , manager=0)
        }
        return render(request , 'orders/show_orders.html' , data)
    else:
         return render(request , 'inspectors/login.html')


def process_responsible(request , id):
    #id for brand
    if request.method == "POST":
        # استقبل قائمة الأيدي كنص مفصول بفواصل
        order_ids_str = request.POST.get('orderids', '')
        # استقبل الموظف المختار (تأكد من أن حقل select به name="employee")
        employee_id = request.POST.get('employee', '')
        
        # قم بتحويل السلسلة إلى قائمة من الأيدي
        orders = order_ids_str.split(',') if order_ids_str else []
        
        # اطبع كل طلب مع الموظف المختار
        
        for order_id in orders:
            print("Order ID:", order_id, "Employee ID:", employee_id)
            update = Report_order.objects.get(id = order_id)
            update.employee_id_id = employee_id
            update.save()
        messages.success(request, "success_update")
        return redirect('show_orders' , id = id)
       
    else:
        return HttpResponse("خطأ في الطلب")
   
def new_order(request , id):
    #id for brand
    if request.user.is_authenticated:

        if request.method =='POST':
            if Report_order.objects.filter(bransh_id_id = request.POST['branch'] , quarter = request.POST['quarter'] ,year = request.POST['year']).exists():
                messages.success(request, "exist")
                return redirect('new_order' , id = id )
            else:
                new = Report_order()
                new.bransh_id_id = request.POST['branch']
                new.employee_id_id = request.POST['employee']
                new.registerDate = date.today()
                new.year = request.POST['year']
                new.quarter = request.POST['quarter']
                new.save()
                messages.success(request, "success_addNewOrder")
                return redirect('show_orders' , id = id )
        #comppanies = Company.objects.all()
        emps = Employee.objects.filter(supervisor = 0 , manager=0)
        current_year = datetime.datetime.now().year

        data = {
            'brand_id': id ,
            'brandLogo' : Brand.objects.get(id = id).logo ,
            'brandName' : Brand.objects.get(id = id).description ,
            'branchs' : Branch.objects.filter(brand_id = id) ,
            'emps' : emps ,
            'username':  request.session['username'] ,
            'img': request.session['img'] ,
            'year': current_year,
        }
        return render(request , 'orders/new_order.html' , data)
    else: # not auth
        return render(request , 'inspectors/login.html')

# def add_brands_orders(request, id):
#         branches = Branch.objects.filter(brand_id = id)
#         for b in branches :
#             new = Report_order()
#             new.bransh_id_id = b.id
#             new.employee_id_id = request.POST['employee']
#             new.registerDate = date.today()
#             new.year = request.POST['year']
#             new.quarter = request.POST['quarter']
#             new.save()
#         messages.success(request, "success_addNewBrandsOrder")
#         return redirect('show_orders' , id = id )


def add_brands_orders(request, id):
    # id for brand 
    # جلب جميع الفروع التابعة للعلامة التجارية
    branches = Branch.objects.filter(brand_id=id)
    total_branches = branches.count()
    created_count = 0

    for branch in branches:
        # التحقق مما إذا كان هناك طلب لهذا الفرع بنفس الربع والسنة
        if Report_order.objects.filter(
            bransh_id_id=branch.id,
            quarter=request.POST['quarter'],
            year=request.POST['year']
        ).exists():
            # الشرط تحقق لهذا الفرع، لا نقوم بحفظ الطلب الجديد
            continue
        else:
            # الشرط لم يتحقق، نقوم بحفظ الطلب الجديد للفرع
            new_order = Report_order()
            new_order.bransh_id_id = branch.id
            new_order.employee_id_id = request.POST['employee']
            new_order.registerDate = date.today()
            new_order.year = request.POST['year']
            new_order.quarter = request.POST['quarter']
            new_order.save()
            created_count += 1
    print(f' عدد الطلبات المنشئة ${created_count}')
    # تقييم النتائج وإرسال الرسالة المناسبة:
    if created_count == total_branches:
        # لم يتحقق الشرط لأي فرع، أي تم حفظ الطلب لجميع الفروع
        messages.success(request, "ok")
        return redirect('show_orders', id=id)
    elif created_count == 0:
        print("انا اشتغلت")
        # تحقق الشرط لجميع الفروع، أي لم يتم حفظ أي طلب جديد
        messages.success(request, "error")
        return redirect('new_order', id=id)
    else:
        # تحقق الشرط لبعض الفروع فقط
        messages.success(request, "notall")
        return redirect('new_order', id=id)

    
   

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


def add_responsibles(request):
    if request.method == "POST":
        # استقبال البيانات
        selected_terms = request.POST.get('selected_terms', '')
        sec_ids = request.POST.getlist('secid[]')
        zone_ids = request.POST.getlist('zoneid[]')
        
        # تقسيم البنود المحددة إلى قائمة
        terms_list = selected_terms.split(',') if selected_terms else []
        
        # لكل تيرم ولكل زوج (sec, zone) نقوم بإنشاء سجل جديد
        for term in terms_list:
            print("Processing term:", term)
            for sec, zone in zip(sec_ids, zone_ids):
                print("Section:", sec, "Zone:", zone)
                if Term_responsible.objects.filter(term_id = term , section_id = sec ,zone_id = zone ).exists():
                     pass
                else:
                    new = Term_responsible()  # إنشاء سجل جديد لكل تكرار
                    new.term_id_id = term
                    new.section_id_id = sec
                    new.zone_id_id = zone
                    new.save()
        messages.success(request, "success")
        return redirect('brand_terms', id=request.POST['brandId'])


        
        # يمكنك الآن متابعة باقي معالجة البيانات
        # ...
def term_cancel(request):
    if request.method == "POST":
        # استقبال البيانات
        selected_terms = request.POST.get('selected_terms', '')
        
        # تقسيم البنود المحددة إلى قائمة
        terms_list = selected_terms.split(',') if selected_terms else []
        
        # لكل تيرم ولكل زوج (sec, zone) نقوم بإنشاء سجل جديد
        for term in terms_list:
            update = Term.objects.get(id = term)  # إنشاء سجل جديد لكل تكرار
            update.cancel = 1
            update.save()
                
        return redirect('brand_terms', id=request.POST['brandId']) 



# اضافة المسؤولين
# غسر مستخدم هذا الفنكشن
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
    
# اضافة الملاحظات
def insert_note(request , brandid , termid):
    #id for term
    # term = Term.objects.get(id = termid)
    new = Term.objects.get(id = termid)
    new.note = request.POST['note']
    new.save()
    print("حفظ  ملاحظة جديد")
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
                'brandName': term.brand_id.description,
                'brandlogo': term.brand_id.logo,
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
                     'order': Report_order.objects.get(id = id)
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


# def calc_order(id):
#     #id for order
#       # جلب جميع السجلات المرتبطة بالطلب المحدد
#     scores = Term_score.objects.filter(report_order_id_id=id)

#     # التحقق من وجود درجات
#     if not scores.exists():
#         return 0  # إذا لم تكن هناك درجات، أعد 0

#     # حساب مجموع الدرجات (والتي هي إما 0 أو 1)
#     total_score = sum(int(score.score) for score in scores)

#     # حساب عدد البنود (terms) وهو العدد الكلي للدرجات الممكنة
#     total_terms = scores.count()

#     # حساب النسبة المئوية وتحويلها إلى عدد صحيح
#     percentage = int((total_score / total_terms) * 100) if total_terms > 0 else 0

#     return percentage

def calc_order(order_id):
    # جلب جميع السجلات المرتبطة بالطلب المحدد
    scores = Term_score.objects.filter(report_order_id_id=order_id)

    # التحقق من وجود درجات
    if not scores.exists():
        return 0  # إذا لم تكن هناك درجات، أعد 0

    # جمع الدرجات الصالحة فقط (التي تكون غير فارغة وقابلة للتحويل إلى عدد صحيح)
    total_score = 0
    valid_terms_count = 0

    for score in scores:
        if score.score.strip():  # التحقق من أن الدرجة غير فارغة
            try:
                total_score += int(score.score)  # إضافة الدرجة إلى المجموع
                valid_terms_count += 1  # زيادة عدد البنود الصالحة
            except ValueError:
                continue  # تجاهل أي درجة لا يمكن تحويلها إلى عدد صحيح

    # حساب النسبة المئوية بناءً على البنود الصالحة فقط
    percentage = round( float((total_score / valid_terms_count) * 100)) if valid_terms_count > 0 else 0

    return percentage


def submit_result(request , resault , orderid):
    ord = Report_order.objects.get(id=orderid)
    new = Score_history()
    new.report_order_id_id = orderid
    new.total_score = resault
    new.quarter = ord.quarter
    new.year = ord.year
    new.registerDate = date.today()
    ord.status = '3' 
    ord.save()
    new.save()
    #تغيير الحاله الى معتمد
    messages.success(request, "ok")
    return redirect('show_order_details' , id=orderid)
    