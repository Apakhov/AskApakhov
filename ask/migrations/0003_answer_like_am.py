# Generated by Django 2.1.2 on 2018-11-06 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0002_auto_20181106_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='like_am',
            field=models.IntegerField(default=0, verbose_name='количество Лукашенко'),
        ),
    ]
