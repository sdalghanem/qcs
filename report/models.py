from django.db import models
from cloudteam.models import *
from clients.models import *
# Create your models here.
 
# الاماكن
class Zone(models.Model):
    name = models.CharField(max_length=100 , verbose_name ='المكان')
    brand_id = models.ForeignKey( Brand, on_delete=models.CASCADE , verbose_name =' العلامة التجارية')
    class Meta:
        verbose_name_plural = "الأماكن"
    def __str__(self):
        return self.name

# البنود
class Term(models.Model):
    description = models.CharField(max_length=100 , verbose_name ='البند')
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE , verbose_name =' العلامة التجارية')
    note = models.CharField(max_length=1500 , verbose_name ='ملاحظات' , null=True)
    cancel = models.BooleanField(default= 0 , null= True)
    class Meta:
        verbose_name_plural = "البند"
    def __str__(self):
        return self.description 

class Term_responsible(models.Model):
    term_id = models.ForeignKey(Term, on_delete=models.CASCADE , verbose_name =' البند')
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE , verbose_name ='  القسم المسؤول' , null=True )
    zone_id = models.ForeignKey(Zone, on_delete=models.CASCADE , verbose_name =' المكان' , null=True )
    class Meta:
        verbose_name_plural = "مسؤولين البنود"
    def __str__(self):
        return self.section_id.description

# التقرير 
# تضيف فيلد جديد تسميه اكتيف يعني اخر تقرير عشان تجيب النتايج منه ويكون 0 -1
class Report_order(models.Model):
    bransh_id = models.ForeignKey( Branch , on_delete=models.CASCADE , verbose_name =' الفرغ')
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE , verbose_name ='  المفتش')
    registerDate = models.DateField(null=True , verbose_name ='تاريخ التسجيل')
    status = models.CharField(max_length=100 , verbose_name ='الحالة', null=True , default= '0')
    quarter = models.CharField(max_length=100 , verbose_name ='الربع' , null= True)
    year = models.CharField(max_length=100 , verbose_name ='السنه' , null= True)
    class Meta:
        verbose_name_plural = 'طلب تقرير'
    def __str__(self):
        return self.bransh_id.description

# تغيير السنه و الربع من جدول الدرجات الى جدول الطلبات للسهولة

# تقييم البنود
class Term_score(models.Model):
    report_order_id = models.ForeignKey( Report_order , on_delete=models.CASCADE , verbose_name =' طلب التقرير')
    term_id = models.ForeignKey(Term, on_delete=models.CASCADE , verbose_name =' البند')
    score = models.CharField(max_length=100 , verbose_name ='الدرجة')
    note = models.CharField(max_length=100 , verbose_name ='الملاحظة' , null= True)
    img = models.FileField(upload_to='customer/terms/Company/brand', verbose_name ='المخالفة' , null= True)
    registerDate = models.DateField(null=True , verbose_name ='تاريخ التسجيل')

    class Meta:
        verbose_name_plural = 'تقييم البنود'
    def __str__(self):
        return self.report_order_id.bransh_id.description

class Score_history(models.Model):
    report_order_id = models.ForeignKey( Report_order , on_delete=models.CASCADE , verbose_name =' طلب التقرير')
    total_score = models.CharField(max_length=100 , verbose_name ='الدرجة النهائية')
    quarter = models.CharField(max_length=100 , verbose_name ='الربع' , null= True)
    year = models.CharField(max_length=100 , verbose_name ='السنه' , null= True)
    registerDate = models.DateField(null=True , verbose_name ='تاريخ التسجيل')
    class Meta:
        verbose_name_plural = 'النتايج النهائية'
    def __str__(self):
        return self.report_order_id.bransh_id.description

class Score_history_department(models.Model):
    report_order_id = models.ForeignKey( Report_order , on_delete=models.CASCADE , verbose_name =' طلب التقرير')
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE , verbose_name ='  القسم ' , null=True )
    total_score = models.CharField(max_length=100 , verbose_name ='الدرجة النهائية')
    quarter = models.CharField(max_length=100 , verbose_name ='الربع' , null= True)
    year = models.CharField(max_length=100 , verbose_name ='السنه' , null= True)
    registerDate = models.DateField(null=True , verbose_name ='تاريخ التسجيل')
    class Meta:
        verbose_name_plural = 'النتايج النهائية'
    def __str__(self):
        return self.report_order_id.bransh_id.description

