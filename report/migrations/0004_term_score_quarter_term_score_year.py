# Generated by Django 4.2.10 on 2024-06-25 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_term_score_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='term_score',
            name='quarter',
            field=models.CharField(max_length=100, null=True, verbose_name='الربع'),
        ),
        migrations.AddField(
            model_name='term_score',
            name='year',
            field=models.CharField(max_length=100, null=True, verbose_name='السنه'),
        ),
    ]
