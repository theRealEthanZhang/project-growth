# Generated by Django 3.2.4 on 2021-07-01 01:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('company_page', '0025_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='file',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]