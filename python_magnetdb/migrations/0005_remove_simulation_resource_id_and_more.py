# Generated by Django 5.0.7 on 2024-07-24 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magnetdb', '0004_alter_simulation_setup_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulation',
            name='resource_id',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='resource_type',
        ),
    ]
