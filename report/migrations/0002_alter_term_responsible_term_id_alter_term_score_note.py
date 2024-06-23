# Generated by Django 4.2.10 on 2024-04-24 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term_responsible',
            name='term_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.term', verbose_name=' البند'),
        ),
        migrations.AlterField(
            model_name='term_score',
            name='note',
            field=models.CharField(max_length=100, null=True, verbose_name='الملاحظة'),
        ),
    ]
