# Generated by Django 3.2.19 on 2023-05-22 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersmodel',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
