# Generated by Django 5.0.1 on 2024-01-27 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraction', '0003_alter_postreaction_is_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='uploads/mediapost'),
        ),
    ]