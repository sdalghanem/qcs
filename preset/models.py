from django.db import models

# Create your models here.
# البنود
class Packege(models.Model):
    description = models.CharField(max_length=100 , verbose_name ='اسم الباقة')
    class Meta:
        verbose_name_plural = "الباقة "

class Term_title(models.Model):
    section = models.CharField(max_length=100 , verbose_name ='القسم')
    packege_id = models.ForeignKey( Packege, on_delete=models.CASCADE , verbose_name =' الباقة')

    class Meta:
        verbose_name_plural = "  الاقسام "

class Preset_terms(models.Model):
    description = models.CharField(max_length=100 , verbose_name ='البند')
    term_title_id = models.ForeignKey( Term_title, on_delete=models.CASCADE , verbose_name =' القسم')
    class Meta:
        verbose_name_plural = " البنود المسبقة "