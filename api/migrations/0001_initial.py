# Generated by Django 5.0 on 2023-12-21 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=1000, verbose_name='title')),
                ('authors', models.CharField(max_length=1000, verbose_name='authors')),
            ],
        ),
    ]
