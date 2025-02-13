# Generated by Django 5.1.6 on 2025-02-13 09:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
        ('users', '0002_alter_user_email_alter_user_name_alter_user_nickname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='users.user'),
        ),
    ]
