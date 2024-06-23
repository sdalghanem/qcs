from django.db import models
from django.contrib.auth.models import User
# ####
# users info :
# admin 1234
# Saad Ss@123123
# ####
# العناوين
class Country(models.Model):
    name = models.CharField(max_length=100 , verbose_name ='الدولة')
    
    class Meta:
        verbose_name_plural = "الدول"

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100 , verbose_name ='المنطقة')
    country_id = models.ForeignKey("Country", on_delete=models.CASCADE , verbose_name =' الدولة')
    
    class Meta:
        verbose_name_plural = "المناطق"

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100 , verbose_name ='المدينة')
    region_id = models.ForeignKey("Region", on_delete=models.CASCADE , verbose_name =' المنطقة')
    
    class Meta:
        verbose_name_plural = "المدن"

    def __str__(self):
        return self.name 

class District(models.Model):
    name = models.CharField(max_length=100 , verbose_name ='الحي')
    city_id = models.ForeignKey("City", on_delete=models.CASCADE , verbose_name =' المدينة')
    
    class Meta:
        verbose_name_plural = "أحياء"

    def __str__(self):
        return self.name

# بيانات الشركة 
class Company(models.Model):
    description = models.CharField(max_length=100 , verbose_name ='اسم الشركة')
    logo = models.FileField(upload_to='customer/profile/Company/logo', null=True , verbose_name ='الشعار')
    registerDate = models.DateField(null=True , verbose_name ='تاريخ التسجيل')
    class Meta:
        verbose_name_plural = "الشركات"

    def __str__(self):
        return self.description

# المدراء
class Managers(models.Model):
    user = models.ForeignKey( User, verbose_name=("اسم المستخدم"), on_delete=models.CASCADE)
    company_id = models.ForeignKey( Company , verbose_name=("الشركة"), on_delete=models.CASCADE)
    mobile = models.CharField(max_length=100 , verbose_name ='رقم الجوال')
    gm_manager = models.BooleanField(default=0)
    task_traker = models.BooleanField(default=0)
    class Meta:
        verbose_name_plural = "المدراء"

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
# الادارة و الاقسام 
class Department(models.Model):
    manager_id = models.ForeignKey( Managers , verbose_name=("مدير الإدارة"),  null= True, on_delete=models.CASCADE)
    description = models.CharField(max_length=100 , verbose_name ='الإدارة')
    company_id = models.ForeignKey( Company , verbose_name=("الشركة"), on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "الإدارات"

    def __str__(self):
        return self.description
    
class Section(models.Model):
    manager_id = models.ForeignKey( Managers , verbose_name=("مدير القسم"),  null= True, on_delete=models.CASCADE)
    description = models.CharField(max_length=100 , verbose_name ='القسم')
    department_id = models.ForeignKey( Department , verbose_name=("الإدارة"), on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "الأقسام"

    def __str__(self):
        return self.description

#الفروع و العلامات التجارية
class Brand(models.Model):
    gm_manager_id = models.ForeignKey( Managers , verbose_name=("مدير عام العلامة التجارية"),  null= True, on_delete=models.CASCADE)
    description = models.CharField(max_length=100 , verbose_name ='العلامة التجارية')
    company_id = models.ForeignKey( Company , verbose_name=("الشركة"), on_delete=models.CASCADE)
    logo = models.FileField(upload_to='customer/profile/Company/brand', null=True , verbose_name ='الشعار')
    registerDate = models.DateField(null=True , verbose_name ='تاريخ التسجيل')
    class Meta:
        verbose_name_plural = "العلامات التجارية"
    def __str__(self):
        return self.description 
    
# مدير منطقة و مدينة
class Brand_regionManager(models.Model):
    manager_id = models.ForeignKey( Managers , verbose_name=("مدير علامة تجارية"),  null= True, on_delete=models.CASCADE)
    Brand_id = models.ForeignKey( Brand , verbose_name=("العلامة التجارية"), on_delete=models.CASCADE)
    region_id = models.ForeignKey( Region , verbose_name=("المنطقة"), on_delete=models.CASCADE)
    registerDate = models.DateField(null=True , verbose_name ='تاريخ التسجيل')
    class Meta:
        verbose_name_plural = "مدراء المناطق"

    def __str__(self):
         return self.manager_id.user.first_name + ' ' + self.manager_id.user.last_name
    
class Brand_cityManager(models.Model):
    manager_id = models.ForeignKey( Managers , verbose_name=("مدير علامة تجارية"),  null= True, on_delete=models.CASCADE)
    Brand_id = models.ForeignKey( Brand , verbose_name=("العلامة التجارية"), on_delete=models.CASCADE)
    city_id = models.ForeignKey( City , verbose_name=("المدينة"), on_delete=models.CASCADE)
    registerDate = models.DateField(null=True , verbose_name ='تاريخ التسجيل')
    class Meta:
        verbose_name_plural = "مدراء المدن"

    def __str__(self):
        return self.manager_id.user.first_name + ' ' + self.manager_id.user.last_name
    
# الفروع
class Branch(models.Model):
    manager_id = models.ForeignKey( Managers , verbose_name=("مدير فرع"),  null= True, on_delete=models.CASCADE)
    description = models.CharField(max_length=100 , verbose_name ='الفرع')
    brand_id = models.ForeignKey( Brand , verbose_name=("العلامة التجارية"), on_delete=models.CASCADE)
    district_id = models.ForeignKey( District , verbose_name=("الحي"), on_delete=models.CASCADE)
    registerDate = models.DateField(null=True , verbose_name ='تاريخ التسجيل')
    class Meta:
        verbose_name_plural = "الفروع"

    def __str__(self):
        return self.description
    
