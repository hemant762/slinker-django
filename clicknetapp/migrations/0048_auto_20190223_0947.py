# Generated by Django 2.1 on 2019-02-23 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clicknetapp', '0047_auto_20190222_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertab',
            name='img',
            field=models.ImageField(default='{{ MEDIA_URL }}user_img/default.png', upload_to='user_img'),
        ),
    ]
