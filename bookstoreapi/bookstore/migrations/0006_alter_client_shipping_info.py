# Generated by Django 3.2 on 2023-07-20 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0005_auto_20230720_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='shipping_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bookstore.shippinginfo', verbose_name='Shipping Info'),
        ),
    ]
