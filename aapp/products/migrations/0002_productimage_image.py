# Generated by Django 5.1.3 on 2024-12-05 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default=None, upload_to='static/images/product_images/'),
            preserve_default=False,
        ),
    ]
