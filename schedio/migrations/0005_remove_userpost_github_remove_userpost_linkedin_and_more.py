# Generated by Django 4.1.7 on 2023-04-03 09:24

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("schedio", "0004_userpost_github_userpost_linkedin_userpost_phone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userpost",
            name="github",
        ),
        migrations.RemoveField(
            model_name="userpost",
            name="linkedin",
        ),
        migrations.RemoveField(
            model_name="userpost",
            name="phone",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="github",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="linkedin",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, null=True, region=None, unique=True
            ),
        ),
    ]