# Generated by Django 3.2.6 on 2021-09-25 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='heart',
            field=models.PositiveIntegerField(default=0),
        ),
    ]