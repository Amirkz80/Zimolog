# Generated by Django 3.2.6 on 2021-10-23 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0010_alter_blogpost_people_who_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
