# Generated by Django 3.2 on 2023-07-31 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0017_alter_bookorder_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.CharField(blank=True, max_length=4, verbose_name='Year'),
        ),
    ]