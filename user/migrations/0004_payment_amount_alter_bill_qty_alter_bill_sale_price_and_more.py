# Generated by Django 5.1.6 on 2025-04-15 03:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='bill',
            name='qty',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='bill',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='pro_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddIndex(
            model_name='bill',
            index=models.Index(fields=['sale', 'product'], name='user_bill_sale_id_2787bb_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['cat_name'], name='user_catego_cat_nam_3ea0aa_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['sale', 'paymethod'], name='user_paymen_sale_id_903129_idx'),
        ),
        migrations.AddIndex(
            model_name='paymethod',
            index=models.Index(fields=['pay_name'], name='user_paymet_pay_nam_8f6b4f_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['user', 'category'], name='user_produc_user_id_6e4912_idx'),
        ),
        migrations.AddIndex(
            model_name='role',
            index=models.Index(fields=['role_name'], name='user_role_role_na_594c3e_idx'),
        ),
        migrations.AddIndex(
            model_name='sale',
            index=models.Index(fields=['sale_code', 'user'], name='user_sale_sale_co_6487cb_idx'),
        ),
    ]
