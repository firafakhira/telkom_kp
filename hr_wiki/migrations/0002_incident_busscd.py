# Generated by Django 2.2.1 on 2019-06-14 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_wiki', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='busscd',
            field=models.IntegerField(default=1000),
            preserve_default=False,
        ),
    ]
