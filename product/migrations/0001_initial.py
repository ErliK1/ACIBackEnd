# Generated by Django 5.0.7 on 2024-08-14 21:58

import django.db.models.deletion
import django.db.models.manager
import product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'brand',
                'verbose_name_plural': 'brandet',
                'db_table': 'brand',
            },
            managers=[
                ('aci_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Kategori',
                'verbose_name_plural': 'Kategoritë',
                'db_table': 'category',
            },
            managers=[
                ('aci_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('transaction_time', models.DateTimeField(default=product.models.get_local_timezone)),
                ('client_secret', models.CharField(blank=True, max_length=100, null=True)),
                ('is_paid_online', models.BooleanField(default=False)),
                ('printed_recipt', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orderat',
                'db_table': 'order',
            },
            managers=[
                ('aci_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('sku_code', models.CharField(max_length=100, unique=True)),
                ('buy_price', models.FloatField()),
                ('sell_price', models.FloatField()),
                ('description', models.TextField(blank=True, null=True)),
                ('stock', models.PositiveIntegerField()),
                ('discount', models.FloatField(default=0)),
                ('has_discount', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.brand')),
            ],
            options={
                'verbose_name': 'Produkt',
                'verbose_name_plural': 'Produktet',
                'db_table': 'products',
            },
            managers=[
                ('aci_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductPopularity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('product_count', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_popularities', to='product.product')),
            ],
            options={
                'db_table': 'product_popularity',
            },
            managers=[
                ('aci_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('product_count', models.IntegerField()),
                ('price', models.IntegerField()),
                ('discount', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='product.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='product.product')),
            ],
            options={
                'verbose_name': 'Order_Product',
                'verbose_name_plural': 'Order_Productet',
                'db_table': 'order_product',
                'unique_together': {('order', 'product')},
            },
            managers=[
                ('aci_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_categories', to='product.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_categories', to='product.product')),
            ],
            options={
                'db_table': 'product_category',
                'unique_together': {('product', 'category')},
            },
            managers=[
                ('aci_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
