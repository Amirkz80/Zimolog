# Generated by Django 3.2.6 on 2021-09-25 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_alter_blogpost_people_who_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='people_who_liked',
            field=models.JSONField(default=['#']),
        ),
    ]
