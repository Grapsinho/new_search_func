# Generated by Django 5.0 on 2023-12-24 18:50

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_remove_product_name_gin_index_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(fields=['name'], name='name_gin_index', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(fields=['description'], name='description_gin_index', opclasses=['gin_trgm_ops']),
        ),
    ]
