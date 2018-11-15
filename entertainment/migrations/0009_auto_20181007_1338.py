# Generated by Django 2.0.5 on 2018-10-07 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entertainment', '0008_auto_20181007_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge_id', models.CharField(max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('email', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_refunded', models.BooleanField(default=False)),
                ('refunded_at', models.DateTimeField(blank=True, null=True)),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'transactions',
            },
        ),
        migrations.AlterModelOptions(
            name='wish',
            options={'ordering': ['-updated_at'], 'verbose_name_plural': 'Lankytojų prašymai'},
        ),
        migrations.AddField(
            model_name='transaction',
            name='wish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entertainment.Wish'),
        ),
    ]