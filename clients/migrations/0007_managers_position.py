# Generated by Django 4.2.10 on 2024-07-14 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_alter_branch_manager_id_alter_brand_gm_manager_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='managers',
            name='position',
            field=models.CharField(max_length=100, null=True, verbose_name='المنصب'),
        ),
    ]
