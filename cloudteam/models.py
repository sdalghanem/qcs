from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# المدراء
class Employee(models.Model):
    user = models.ForeignKey( User, verbose_name=("اسم المستخدم"), on_delete=models.CASCADE)
    mobile = models.CharField(max_length=100 , verbose_name ='رقم الجوال')
    supervisor = models.BooleanField(default=0)
    manager = models.BooleanField(default=0)
    profile_img = models.FileField(upload_to='cloudtem/profile', null=True , verbose_name ='الصورة الشخصية')
    class Meta:
        verbose_name_plural = "الموظفين"

    def __str__(self):
        return self.user.first_name + '' + self.user.last_name
    
# الادارة و الاقسام 
class cloudteam_Department(models.Model):
    manager_id = models.ForeignKey( Employee , verbose_name=("مدير الإدارة"),  null= True, on_delete=models.CASCADE)
    description = models.CharField(max_length=100 , verbose_name ='الإدارة')
    class Meta:
        verbose_name_plural = "الإدارات"

    def __str__(self):
        return self.description
    
class cloudteam_Section(models.Model):
    manager_id = models.ForeignKey( Employee , verbose_name=("مشرف القسم"),  null= True, on_delete=models.CASCADE)
    description = models.CharField(max_length=100 , verbose_name ='القسم')
    department_id = models.ForeignKey( cloudteam_Department , verbose_name=("الإدارة"), on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "الأقسام"

    def __str__(self):
        return self.description
