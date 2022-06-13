# Generated by Django 4.0.3 on 2022-06-05 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_bid_price', models.PositiveIntegerField()),
                ('bid_start', models.DateTimeField()),
                ('bid_expiry', models.DateTimeField()),
                ('min_required_credit', models.PositiveIntegerField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
                ('category_description', models.CharField(max_length=900)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=300)),
                ('product_description', models.CharField(max_length=900)),
                ('verified', models.DateTimeField(auto_now_add=True)),
                ('bid_start', models.DateTimeField()),
                ('bid_expiry', models.DateTimeField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auction.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
                ('verified_by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_verified', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid_Trasaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('has_won', models.BooleanField()),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.auction')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='auction',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auction.product'),
        ),
    ]