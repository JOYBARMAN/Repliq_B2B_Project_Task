# Generated by Django 4.1.5 on 2023-06-06 07:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')], default='pending', max_length=100)),
                ('source_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_connection', to='shop.shop')),
                ('target_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_connection', to='shop.shop')),
            ],
        ),
    ]
