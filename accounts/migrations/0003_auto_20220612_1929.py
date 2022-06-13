# Generated by Django 3.2.4 on 2022-06-12 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220608_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_image',
            field=models.ImageField(default='default.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('SELLER', 'Seller'), ('BUYER', 'Buyer')], max_length=200),
        ),
    ]
