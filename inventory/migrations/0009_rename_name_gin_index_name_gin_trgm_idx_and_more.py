# Generated by Django 5.0 on 2023-12-24 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_product_name_gin_index_product_description_gin_index'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='product',
            new_name='name_gin_trgm_idx',
            old_name='name_gin_index',
        ),
        migrations.RenameIndex(
            model_name='product',
            new_name='description_gin_trgm_idx',
            old_name='description_gin_index',
        ),
    ]
