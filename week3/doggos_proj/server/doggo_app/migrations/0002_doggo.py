# Generated by Django 2.2.4 on 2019-12-10 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doggo_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doggo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('bio', models.TextField()),
                ('age', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('tricks', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('submitted_by', models.ForeignKey(on_delete='CASCADE', related_name='dogs', to='doggo_app.User')),
            ],
        ),
    ]
