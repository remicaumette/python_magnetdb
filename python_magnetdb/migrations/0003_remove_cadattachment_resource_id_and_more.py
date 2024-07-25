# Generated by Django 5.0.7 on 2024-07-24 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magnetdb', '0002_cadattachment_magnet_cadattachment_part_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cadattachment',
            name='resource_id',
        ),
        migrations.RemoveField(
            model_name='cadattachment',
            name='resource_type',
        ),
        migrations.AddField(
            model_name='magnet',
            name='simulations',
            field=models.ManyToManyField(related_name='magnet_simulations', to='magnetdb.simulation'),
        ),
        migrations.AddField(
            model_name='simulation',
            name='magnet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='magnetdb.magnet'),
        ),
        migrations.AddField(
            model_name='simulation',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='magnetdb.site'),
        ),
        migrations.AddField(
            model_name='site',
            name='simulations',
            field=models.ManyToManyField(related_name='site_simulations', to='magnetdb.simulation'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='setup_state',
            field=models.JSONField(default={}),
        ),
    ]