# Generated by Django 2.0.5 on 2018-10-03 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_auto_20181003_1554'),
        ('entertainment', '0005_wish_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='writers',
            field=models.ManyToManyField(to='library.Writer'),
        ),
    ]