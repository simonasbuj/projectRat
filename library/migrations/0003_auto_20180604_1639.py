# Generated by Django 2.0.5 on 2018-06-04 13:39

from django.db import migrations, models
import django.db.models.deletion
import library.helper


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20180604_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('death_date', models.DateField()),
            ],
            options={
                'db_table': 'writers',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(default='testas', editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=library.helper.book_cover_upload),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.Category'),
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(blank=True, to='library.Tag'),
        ),
        migrations.AddField(
            model_name='book',
            name='writers',
            field=models.ManyToManyField(to='library.Writer'),
        ),
    ]
