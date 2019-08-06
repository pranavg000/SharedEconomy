# Generated by Django 2.2.2 on 2019-08-01 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190729_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='itemsPaidFor',
            field=models.ManyToManyField(blank=True, related_name='itemsPaidFor', to='core.Product'),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='itemsInCart',
            field=models.ManyToManyField(blank=True, related_name='itemsInCart', to='core.Product'),
        ),
    ]