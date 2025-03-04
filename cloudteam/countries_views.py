from django.shortcuts import redirect, render
from clients.models import * 
# اضافه بروفايل شركة
# اضافة براند
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from preset.models import *
from report.models import *
from django.contrib import messages
import json
from django.contrib.auth import authenticate , login as auth_login , logout
from datetime import date

def show_region(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            if Region.objects.filter(name = request.POST['region']).exists():
                 messages.success(request, "exist")
                 return redirect('show_region')
            else:
                new = Region()
                new.name =  request.POST['region']
                new.country_id_id = 1
                new.save()
                messages.success(request, "success")
                return redirect('show_region')
        regions = Region.objects.filter(country_id = 1)
        data = {
            'username':  request.session['username'] ,
            'img': request.session['img'] ,
            'regions' : regions
        }
        return render(request , 'countries/show_region.html', data)
    else:
        return render(request , 'inspectors/login.html')

def delete_region(request , id):
    if City.objects.filter(region_id_id = id).exists():
            messages.success(request, "exist_cities")
            return redirect('show_region')
    else :
            Region.objects.get(id = id).delete()
            messages.success(request, "delete")
            return redirect('show_region')


        


def show_city(request , id):
    if request.user.is_authenticated:
        #id for rigon 
        cityinfo = []
        row = []
        cities = City.objects.filter(region_id = id)
        for c in cities :
            dist = District.objects.filter(city_id_id = c.id)
            row = {
                'cName' : c.name , 
                'cDist' : dist ,
                'cid': c.id ,
            }
            cityinfo.append(row)
        region = Region.objects.get(id = id)
        data = {
            'username':  request.session['username'] ,
            'img': request.session['img'] ,
            'cities' : cityinfo , 
            'regionName' : region.name ,
            'regionID': region.id
        }
        return render(request , 'countries/show_city.html', data)
    else :
        return render(request , 'inspectors/login.html')

def add_city(request):
     if request.user.is_authenticated:
        if request.method =='POST':
            # check name
            if City.objects.filter(region_id_id =request.POST['regionID'] , name=request.POST['city'] ).exists():
                 messages.success(request, "exist")
                 return redirect('show_city' , id = request.POST['regionID'])
            else:
                # save new
                new = City()
                new.name = request.POST['city']
                new.region_id_id = request.POST['regionID']
                new.save()
                messages.success(request, "success")
                return redirect('show_city' , id = request.POST['regionID'])
        else:
            return render(request , 'inspectors/login.html')


def add_district(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            if District.objects.filter(name = request.POST['district'] , city_id_id = request.POST['cid'] ).exists():
                messages.success(request, "exist_distName")
                return redirect('show_city' , id = request.POST['regionID'])
            else:
                new = District()
                new.name = request.POST['district']
                new.city_id_id = request.POST['cid']
                new.save()
                messages.success(request, "success_dist")
                return redirect('show_city' , id = request.POST['regionID'])
           ##########
            # cityinfo = []
            # row = []
            # cities = City.objects.filter(region_id_id = request.POST['regionID'])
            # for c in cities :
            #     dist = District.objects.filter(city_id_id = c.id)
            #     row = {
            #         'cName' : c.name , 
            #         'cDist' : dist ,
            #         'cid': c.id ,
            #     }
            #     cityinfo.append(row)
            # region = Region.objects.get(id = request.POST['regionID'])
            # data = {
            #     'username':  request.session['username'] ,
            #     'img': request.session['img'] ,
            #     'cities' : cityinfo , 
            #     'regionName' : region.name ,
            #     'regionID': region.id ,
            #     'res': res
            # }
            # return render(request , 'countries/show_city.html', data)
    
    else:
        return render(request , 'inspectors/login.html')


def delete_city(request , id):
    city = City.objects.get(id = id)
    regionID = city.region_id.id
    #id for city
    if District.objects.filter(city_id_id = id).exists():
        messages.success(request, "exist_dist")
        return redirect('show_city', id = regionID)
    else:
        city.delete()
        messages.success(request, "delete")
        return redirect('show_city', id = regionID)

def delete_district(request , id):
    dist = District.objects.get(id = id)
    regionID = dist.city_id.region_id.id
    #id for dist
    if Branch.objects.filter(district_id_id = id).exists():
        messages.success(request, "exist_branch")
        return redirect('show_city', id = regionID)
    else:
        dist.delete()
        messages.success(request, "delete_dist")
        return redirect('show_city', id = regionID)