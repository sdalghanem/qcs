# Generated by Django 4.2.10 on 2024-08-22 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_remove_managers_task_traker_section_brand_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='managers',
            name='gm_manager',
        ),
    ]
