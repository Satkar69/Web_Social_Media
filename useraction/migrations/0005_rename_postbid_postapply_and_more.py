# Generated by Django 5.0.1 on 2024-01-30 13:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraction', '0004_alter_post_media'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostBid',
            new_name='PostApply',
        ),
        migrations.RenameField(
            model_name='postapply',
            old_name='bid_by',
            new_name='applied_by',
        ),
    ]
