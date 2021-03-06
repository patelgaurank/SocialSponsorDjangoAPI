# Generated by Django 3.1 on 2021-12-07 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20211205_2028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newuserinfo',
            old_name='NewUserInfo_Id',
            new_name='NewUserInfo_ID',
        ),
        migrations.RemoveField(
            model_name='newuserinfo',
            name='currentTimeStamp',
        ),
        migrations.CreateModel(
            name='ZoneLeader',
            fields=[
                ('ZoneLeader_ID', models.AutoField(primary_key=True, serialize=False)),
                ('IMS_Member_ID', models.IntegerField(blank=True, null=True, verbose_name='IMS Id')),
                ('prefix', models.CharField(blank=True, max_length=120, null=True, verbose_name='First Name')),
                ('first_name', models.CharField(blank=True, max_length=120, null=True, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Middle Name')),
                ('last_name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Last Name')),
                ('notes', models.CharField(blank=True, max_length=300, null=True, verbose_name='Notes relate to user')),
                ('Zone', models.CharField(blank=True, max_length=120, null=True, verbose_name='Zone Name')),
                ('Direction', models.CharField(blank=True, max_length=120, null=True, verbose_name='Zone Direction')),
                ('comments', models.CharField(blank=True, max_length=300, null=True, verbose_name='Any Comments?')),
                ('UpdatedDate', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('Entered_By', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Zone_Leader_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Zone Leader info',
                'ordering': ('-created_at',),
            },
        ),
    ]
