# Generated by Django 3.1 on 2021-12-12 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_newuseraddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuserinfo',
            name='Address1',
        ),
        migrations.RemoveField(
            model_name='newuserinfo',
            name='Address2',
        ),
        migrations.RemoveField(
            model_name='newuserinfo',
            name='City',
        ),
        migrations.RemoveField(
            model_name='newuserinfo',
            name='Country',
        ),
        migrations.RemoveField(
            model_name='newuserinfo',
            name='State',
        ),
        migrations.RemoveField(
            model_name='newuserinfo',
            name='ZipCode',
        ),
    ]
