# Generated by Django 2.1 on 2019-02-16 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clicknetapp', '0034_auto_20190216_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='refertable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('referredby', models.ForeignKey(on_delete=True, to='clicknetapp.usertab')),
            ],
        ),
    ]
