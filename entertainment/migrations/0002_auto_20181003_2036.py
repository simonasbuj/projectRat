# Generated by Django 2.0.5 on 2018-10-03 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entertainment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wish',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelTable(
            name='wish',
            table='wishes',
        ),
    ]
