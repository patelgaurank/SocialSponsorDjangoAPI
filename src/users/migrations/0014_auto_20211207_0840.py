# Generated by Django 3.1 on 2021-12-07 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20211207_0839'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newuserinfo',
            options={'ordering': ('-created_at',), 'verbose_name_plural': 'User info'},
        ),
        migrations.AlterModelOptions(
            name='zoneinfo',
            options={'ordering': ('-created_at',), 'verbose_name_plural': 'Zone info'},
        ),
    ]