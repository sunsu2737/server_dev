# Generated by Django 2.2.5 on 2021-08-08 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='user_id',
            field=models.CharField(default=False, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='user_pw',
            field=models.CharField(default=False, max_length=256),
        ),
    ]