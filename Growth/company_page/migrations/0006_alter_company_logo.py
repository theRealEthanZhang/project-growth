# Generated by Django 3.2.4 on 2021-06-05 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_page', '0005_auto_20210605_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to=''),
        ),
    ]
