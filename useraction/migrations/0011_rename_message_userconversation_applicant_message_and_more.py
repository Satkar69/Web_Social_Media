# Generated by Django 5.0.1 on 2024-01-31 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraction', '0010_userconversation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userconversation',
            old_name='message',
            new_name='applicant_message',
        ),
        migrations.AddField(
            model_name='userconversation',
            name='user_message',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
