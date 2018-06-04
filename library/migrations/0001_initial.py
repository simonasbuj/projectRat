# Generated by Django 2.0.5 on 2018-06-04 09:52

from django.db import migrations, models
import library.helper


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('cover', models.ImageField(upload_to=library.helper.book_cover_upload)),
            ],
            options={
                'db_table': 'books',
            },
        ),
    ]
