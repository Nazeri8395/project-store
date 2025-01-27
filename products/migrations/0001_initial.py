# Generated by Django 5.1.5 on 2025-01-27 08:00

import django.db.models.deletion
import django.utils.timezone
import products.utils
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("brand_title", models.CharField(max_length=100)),
                (
                    "image_name",
                    models.ImageField(upload_to=products.utils.FileUpload.upload_to),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Feature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("feature_name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "image_name",
                    models.ImageField(upload_to=products.utils.FileUpload.upload_to),
                ),
                ("price", models.PositiveBigIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("register_date", models.DateTimeField(auto_now=True)),
                (
                    "published_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="brands_of_groups",
                        to="products.brand",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductFeature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=100)),
                (
                    "feature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.feature",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductGallery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image_name",
                    models.ImageField(upload_to=products.utils.FileUpload.upload_to),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("group_title", models.CharField(max_length=100)),
                (
                    "image_name",
                    models.ImageField(upload_to=products.utils.FileUpload.upload_to),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("register_date", models.DateTimeField(auto_now=True)),
                (
                    "published_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "group_parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="groups",
                        to="products.productgroup",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="product_group",
            field=models.ManyToManyField(
                related_name="product_of_groups", to="products.productgroup"
            ),
        ),
        migrations.AddField(
            model_name="feature",
            name="product_group",
            field=models.ManyToManyField(
                related_name="feature_of_group", to="products.productgroup"
            ),
        ),
    ]
