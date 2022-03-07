# Generated by Django 3.1 on 2021-12-06 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20211205_2015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newuserinfo',
            old_name='Zone',
            new_name='Zone_name',
        ),
        migrations.AddField(
            model_name='newuserinfo',
            name='so_lead_karyakar',
            field=models.CharField(blank=True, choices=[('Yes', 'Y'), ('No', 'N')], default='N', max_length=4, null=True, verbose_name='Is he/she so lead karyakar?'),
        ),
        migrations.AddField(
            model_name='newuserinfo',
            name='so_lead_karyakar_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='SO_Lead_Karyakar_Zone_Name', to='users.zone'),
        ),
        migrations.AddField(
            model_name='zone',
            name='notes',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Notes relate to Zone'),
        ),
    ]