# Generated by Django 4.2.6 on 2024-01-15 13:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('roungnakhone_hotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.CharField(max_length=15),
        ),
    ]
