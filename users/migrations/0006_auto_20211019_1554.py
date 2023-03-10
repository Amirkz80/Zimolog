# Generated by Django 3.2.6 on 2021-10-19 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userinfo_bio_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='bio_text',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='picture',
            field=models.ImageField(blank=True, default=False, upload_to='images/'),
        ),
    ]
