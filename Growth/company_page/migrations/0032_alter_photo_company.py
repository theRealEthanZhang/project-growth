# Generated by Django 3.2.4 on 2021-07-01 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company_page', '0031_auto_20210630_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company_page.company'),
        ),
    ]