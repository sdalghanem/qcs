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

def show_country(request):
    regions = Region.objects.filter(country_id = 1)
    data = {
        'username':  request.session['username'] ,
        'img': request.session['img'] ,
        'regions' : regions
    }
    return render(request , 'countries/show_country.html', data)

def show_city(request , id):
    #id for rigon 
    cities = City.objects.filter(region_id = id)
    regionNmae =   Region.objects.get(id = id).name
    data = {
        'username':  request.session['username'] ,
        'img': request.session['img'] ,
        'cities' : cities , 
        'regionName' : regionNmae
    }
    return render(request , 'countries/show_city.html', data)