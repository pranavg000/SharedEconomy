# Generated by Django 2.0.1 on 2019-08-05 19:54

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_productbuyer_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='traveller',
            name='maxAlloc',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='location',
            field=django_countries.fields.CountryField(max_length=2),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='destination',
            field=django_countries.fields.CountryField(max_length=2),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='itemsToBuy',
            field=models.ManyToManyField(null=True, to='core.Product'),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='origin',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]