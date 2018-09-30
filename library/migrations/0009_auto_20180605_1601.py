# Generated by Django 2.0.5 on 2018-06-05 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_auto_20180605_1057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-added_at']},
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='writer',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]