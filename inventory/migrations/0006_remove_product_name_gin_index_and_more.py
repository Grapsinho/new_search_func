# Generated by Django 5.0 on 2023-12-23 21:29

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_remove_product_inventory_p_name_f6a6a1_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='product',
            name='name_gin_index',
        ),
        migrations.RemoveIndex(
            model_name='product',
            name='description_gin_index',
        ),
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(fields=['name'], name='name_gin_index', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(fields=['description'], name='description_gin_index', opclasses=['gin_trgm_ops']),
        ),
    ]
