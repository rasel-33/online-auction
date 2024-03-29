# Generated by Django 4.1 on 2022-09-25 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_profile_is_varified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credittransaction',
            name='transaction_type',
            field=models.CharField(blank=True, choices=[('CREDIT_RETURN', 'Bid Credit Return'), ('REQUESTED_CREDIT', 'Requested Credit'), ('PLACE_BID', 'Place Bid'), ('WIDTHDRAW', 'Widthdraw')], max_length=200, null=True),
        ),
    ]
