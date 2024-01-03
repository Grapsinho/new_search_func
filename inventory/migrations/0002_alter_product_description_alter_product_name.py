# Generated by Django 5.0 on 2023-12-23 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(db_index=True, help_text='format: required', verbose_name='product description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, help_text='format: required, max-255', max_length=255, verbose_name='product name'),
        ),
    ]
