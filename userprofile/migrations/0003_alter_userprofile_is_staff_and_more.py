# Generated by Django 5.0.1 on 2024-01-23 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_userprofile_first_name_userprofile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_staff',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_superuser',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
