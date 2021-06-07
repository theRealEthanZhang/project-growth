# Generated by Django 3.2.4 on 2021-06-06 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_page', '0016_alter_company_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='size',
            field=models.CharField(choices=[('0-3', '0-3 employees'), ('4-6', '4-6 employees'), ('6-10', '6-10 employees'), ('10-20 employees', '10-20 employees'), ('20+', '20+ employees')], default='0-3', max_length=20),
        ),
    ]
