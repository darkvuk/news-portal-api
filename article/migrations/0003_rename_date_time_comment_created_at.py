# Generated by Django 5.0.4 on 2024-04-28 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_comment_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='date_time',
            new_name='created_at',
        ),
    ]
