# Generated by Django 2.1 on 2019-02-10 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clicknetapp', '0023_auto_20190210_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='blc',
            field=models.FloatField(default=0),
        ),
    ]
