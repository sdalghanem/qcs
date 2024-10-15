from django.shortcuts import redirect, render
from clients.models import * 
# اضافه بروفايل شركة
# اضافة براند
from django.http import HttpRequest, HttpResponse, JsonResponse , HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from preset.models import *
from report.models import *
import json
from django.contrib.auth import authenticate , login as auth_login , logout
from datetime import date

def login_insp(request):

    if  request.method =='POST':
                mngUsername = request.POST['username']
                mngPassword = request.POST['password']
                result = authenticate(username = mngUsername , password = mngPassword)
               
                if result is not None:
                    userInfo = User.objects.get(username = mngUsername)

                    if Employee.objects.filter(user_id = userInfo.id , supervisor = '0').exists():
                        emp = Employee.objects.get(user_id = userInfo.id , supervisor = '0')
                        auth_login(request, result) 
                        # save data on session
                        request.session['id'] = emp.id
                        request.session['firestName'] = userInfo.first_name
                        request.session['lastName'] = userInfo.last_name   
                        request.session['username'] = userInfo.username
                        request.session['img'] = str(emp.profile_img)
                        return redirect('/cloudteam/emp_orders')
                    else:
                        return render(request , 'inspectors/employee/login_insp.html' , {'res' : 'ليس لديك صلاحية'})

                else :
                     return render(request , 'inspectors/employee/login_insp.html' , {'res' : 'كلمة المرور او اسم المستخدم غير صحيح'})
                     
    return render(request,'inspectors/employee/login_insp.html')



def emp_orders(request):
      orders = Report_order.objects.filter(employee_id_id = request.session['id'])
      #print(request.session['id'])
      data ={
        'username':  request.session['username'] ,
        'img': request.session['img'] ,
        'orders': orders
      }
      return render(request , 'inspectors/employee/home.html' , data) 

def evaluate(request , id):
      # id for report order
      order = Report_order.objects.get(id = id)
      brandid = order.bransh_id.brand_id
      zones = Zone.objects.filter(brand_id = brandid)
      orNum = order.id 
      orBrn = order.bransh_id.description
      orDate = order.registerDate
      orStatus = order.status
      data ={
        'username':  request.session['username'] ,
        'img': request.session['img'] ,
        'zones': zones ,
        'orNum': orNum,
        'orBrn': orBrn,
        'orDate' : orDate,
        'orStatus': orStatus , # حالة الطلب 
        'orID': order.id
      }
      return render(request , 'inspectors/employee/evaluate.html' , data) 

def get_evaluation_points(request, zone_id , orID):
    # افترض أن البنود الخاصة بكل منطقة مخزنة في قاعدة البيانات
    # جلب البيانات بناءً على معرف المكان (zone_id)
    terms = Term_responsible.objects.filter(zone_id = zone_id)
    zoneName = Zone.objects.get(id = zone_id).name
    print(terms)
    row = []
    for t in terms :
        if Term_score.objects.filter(term_id_id = t.term_id.id , report_order_id_id = orID).exists():
          score = Term_score.objects.get(term_id = t.term_id.id , report_order_id_id = orID).score
          row.append({'term' : t.term_id.description ,'term_id': t.term_id.id , 'status' : '0' , 'score': score})
        else:
            row.append({'term' : t.term_id.description ,'term_id': t.term_id.id })
    print(row)  
    data = {
    'username':  request.session['username'] ,
    'img': request.session['img'] ,
    'row' : row,
    'zoneName': zoneName,
    'orID' : orID
      }

    if  request.method =='POST':
        if  'img0' in request.FILES:
            uploaded_file = request.FILES['img0']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(filename)
        else:
            uploaded_file_url = ''  # إذا لم يكن هناك ملف مرفوع، يكون الرابط فارغًا
   
        termid = request.POST['termid']
        eva = request.POST['evaluation']
        note = request.POST['note']
        print(eva)
        new = Term_score()
        new.report_order_id_id = orID
        new.term_id_id = termid
        new.score = eva
        new.img = uploaded_file_url
        new.note = note
        new.registerDate = date.today()
        new.save()
        #  تغيير حالة الطلب من 0 الى 1 غير مكتمل
        if Report_order.objects.filter(id = orID , status = '1').exists():
        # return redirect('/cloudteam/get_evaluation_points/' ,zone_id = zone_id , orID = orID )
          return HttpResponseRedirect(request.get_full_path())
        else:
           ord = Report_order.objects.get(id = orID)
           ord.status = '1'
           ord.save()
           return HttpResponseRedirect(request.get_full_path())
             
    else:
       
        return render (request , 'inspectors/employee/evaluate_terms.html' , data)
        # هنا يمكنك إرجاع البيانات الحقيقية بناءً على معرف المكان
        # return JsonResponse({"points": row} , safe=False )


def save_evaluation(request , id):
      ord = Report_order.objects.get(id = id)
      ord.status = '2'
      ord.save()
      return redirect('evaluate' , id=id)
