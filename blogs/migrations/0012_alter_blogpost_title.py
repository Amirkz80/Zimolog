# Generated by Django 3.2.6 on 2021-10-23 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_alter_blogpost_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
