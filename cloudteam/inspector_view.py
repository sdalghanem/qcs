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
      print(request.session['id'])
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
      data ={
        'username':  request.session['username'] ,
        'img': request.session['img'] ,
        'zones': zones
      }
      return render(request , 'inspectors/employee/evaluate.html' , data) 