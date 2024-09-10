from django.db import models

# Create your models here.
# البنود
class Packege(models.Model):
    description = models.CharField(max_length=100 , verbose_name ='اسم الباقة')
    class Meta:
        verbose_name_plural = " الباقات"
    def __str__(self):
        return self.description


class Term_title(models.Model):
    section = models.CharField(max_length=100 , verbose_name ='التصنيفات')
    packege_id = models.ForeignKey( Packege, on_delete=models.CASCADE , verbose_name =' الباقة')

    class Meta:
        verbose_name_plural = "  الاقسام "
    def __str__(self):
        return self.section

class Preset_terms(models.Model):
    description = models.CharField(max_length=100 , verbose_name ='البند')
    term_title_id = models.ForeignKey( Term_title, on_delete=models.CASCADE , verbose_name =' التصنيف')
    class Meta:
        verbose_name_plural = " البنود المسبقة "
    def __str__(self):
        return self.description
    