# Generated by Django 3.2 on 2023-07-26 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0012_auto_20230726_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='books',
            field=models.ManyToManyField(related_name='orders', through='bookstore.BookOrder', to='bookstore.Book', verbose_name='Books'),
        ),
    ]