# Generated by Django 4.2.10 on 2024-04-22 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_branch_manager_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='gm_manager_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.managers', verbose_name='اسم المستخدم'),
        ),
        migrations.AddField(
            model_name='department',
            name='manager_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.managers', verbose_name='اسم المستخدم'),
        ),
        migrations.AddField(
            model_name='managers',
            name='gm_manager',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='managers',
            name='task_traker',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='section',
            name='manager_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.managers', verbose_name='اسم المستخدم'),
        ),
        migrations.CreateModel(
            name='Brand_regionManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registerDate', models.DateField(null=True, verbose_name='تاريخ التسجيل')),
                ('Brand_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.brand', verbose_name='العلامة التجارية')),
                ('manager_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.managers', verbose_name='اسم المستخدم')),
                ('region_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.region', verbose_name='المنطقة')),
            ],
            options={
                'verbose_name_plural': 'مدراء المناطق',
            },
        ),
        migrations.CreateModel(
            name='Brand_cityManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registerDate', models.DateField(null=True, verbose_name='تاريخ التسجيل')),
                ('Brand_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.brand', verbose_name='العلامة التجارية')),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.city', verbose_name='المدينة')),
                ('manager_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.managers', verbose_name='اسم المستخدم')),
            ],
            options={
                'verbose_name_plural': 'مدراء المدن',
            },
        ),
    ]
