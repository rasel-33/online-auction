# Generated by Django 3.2.4 on 2022-06-09 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auto_20220608_2244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bidtransaction',
            old_name='user',
            new_name='bidder',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='user',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='verified',
            new_name='verified_time',
        ),
    ]
