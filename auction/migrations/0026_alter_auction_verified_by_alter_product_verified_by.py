# Generated by Django 4.1 on 2022-09-24 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0025_auction_is_varified_auction_verified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='verified_by',
            field=models.CharField(blank=True, choices=[('rasel', 'Rasel'), ('shihab', 'Shihab'), ('sharmin', 'Sharmin')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='verified_by',
            field=models.CharField(blank=True, choices=[('rasel', 'Rasel'), ('shihab', 'Shihab'), ('sharmin', 'Sharmin')], max_length=200, null=True),
        ),
    ]
