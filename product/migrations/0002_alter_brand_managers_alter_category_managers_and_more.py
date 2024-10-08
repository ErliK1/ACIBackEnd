# Generated by Django 5.0.7 on 2024-09-21 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='brand',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='category',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='order',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='orderproduct',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='product',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='productcategory',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='productpopularity',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product.product')),
            ],
            options={
                'verbose_name': 'Imazh Produkti',
                'verbose_name_plural': 'Imazhet e Produktit',
                'db_table': 'product_image',
            },
        ),
    ]
