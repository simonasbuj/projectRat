# Generated by Django 2.0.5 on 2018-06-12 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_auto_20180605_1601'),
        ('accounts', '0005_auto_20180612_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='bookmarks',
            field=models.ManyToManyField(to='library.Book'),
        ),
    ]
