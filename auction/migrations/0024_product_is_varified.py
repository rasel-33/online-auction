# Generated by Django 4.1 on 2022-09-24 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0023_remove_auction_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_varified',
            field=models.BooleanField(null=True),
        ),
    ]
