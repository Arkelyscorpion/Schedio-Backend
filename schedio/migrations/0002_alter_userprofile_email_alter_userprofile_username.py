# Generated by Django 4.1 on 2023-01-29 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schedio", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="username",
            field=models.CharField(max_length=60, unique=True),
        ),
    ]