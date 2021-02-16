# Generated by Django 2.1.5 on 2019-03-03 05:49

import clicknetapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clicknetapp', '0049_auto_20190223_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='static',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=clicknetapp.models.static.indiantime)),
                ('click', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=True, to='clicknetapp.usertab')),
            ],
        ),
    ]
