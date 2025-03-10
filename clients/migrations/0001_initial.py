# Generated by Django 4.2.10 on 2024-04-21 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='المدينة')),
            ],
            options={
                'verbose_name_plural': 'المناطق',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='الدولة')),
            ],
            options={
                'verbose_name_plural': 'الدول',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='المنطقة')),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.country', verbose_name=' الدولة')),
            ],
            options={
                'verbose_name_plural': 'المناطق',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='الحي')),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.city', verbose_name=' المدينة')),
            ],
            options={
                'verbose_name_plural': 'الحي',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='region_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.region', verbose_name=' المنطقة'),
        ),
    ]
