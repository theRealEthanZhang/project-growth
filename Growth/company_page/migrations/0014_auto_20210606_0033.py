# Generated by Django 3.2.4 on 2021-06-06 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_page', '0013_alter_company_website_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, default='default_company_logo.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='company',
            name='website_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]