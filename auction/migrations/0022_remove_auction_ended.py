# Generated by Django 4.1 on 2022-09-24 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0021_alter_auction_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='ended',
        ),
    ]
