# Generated by Django 4.1.5 on 2023-06-19 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='shop',
            new_name='organization',
        ),
    ]