# Generated by Django 3.2.4 on 2021-07-01 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company_page', '0026_auto_20210701_0132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='date_posted',
            new_name='data_added',
        ),
    ]
