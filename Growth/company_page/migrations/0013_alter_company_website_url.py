# Generated by Django 3.2.4 on 2021-06-06 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_page', '0012_alter_company_website_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='website_url',
            field=models.URLField(),
        ),
    ]
