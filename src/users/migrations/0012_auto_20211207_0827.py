# Generated by Django 3.1 on 2021-12-07 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20211207_0821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newuserinfo',
            old_name='IMS_Member_ID',
            new_name='IMS_Member_Id',
        ),
        migrations.RenameField(
            model_name='newuserinfo',
            old_name='NewUserInfo_ID',
            new_name='NewUserInfo_Id',
        ),
        migrations.RenameField(
            model_name='zoneleader',
            old_name='IMS_Member_ID',
            new_name='IMS_Member_Id',
        ),
        migrations.RenameField(
            model_name='zoneleader',
            old_name='ZoneLeader_ID',
            new_name='ZoneLeader_Id',
        ),
    ]
