# Generated by Django 3.2.6 on 2021-10-19 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userinfo_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='bio_text',
            field=models.CharField(default='', max_length=150),
        ),
    ]
