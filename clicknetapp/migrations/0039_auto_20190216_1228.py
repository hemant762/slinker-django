# Generated by Django 2.1 on 2019-02-16 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clicknetapp', '0038_auto_20190216_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refertable',
            name='user',
        ),
        migrations.AddField(
            model_name='usertab',
            name='referredby',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='refertable',
        ),
    ]
