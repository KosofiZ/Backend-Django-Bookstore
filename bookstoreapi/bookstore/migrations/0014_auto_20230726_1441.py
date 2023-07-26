# Generated by Django 3.2 on 2023-07-26 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0013_order_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='books/images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=2, verbose_name='Rating'),
        ),
    ]
