# Generated by Django 2.2.4 on 2019-12-11 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doggo_app', '0003_doggo_is_good_boy'),
    ]

    operations = [
        migrations.AddField(
            model_name='doggo',
            name='profile_pic_url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
