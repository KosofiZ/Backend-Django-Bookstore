# Generated by Django 3.2 on 2023-07-30 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0016_alter_client_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookorder',
            options={'verbose_name': 'Book order', 'verbose_name_plural': 'Book order'},
        ),
    ]
