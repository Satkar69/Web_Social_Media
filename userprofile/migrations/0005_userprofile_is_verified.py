# Generated by Django 5.0.1 on 2024-01-23 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_alter_userprofile_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_verified',
            field=models.BooleanField(default=True),
        ),
    ]