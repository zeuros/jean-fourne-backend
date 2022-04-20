from django.db import migrations

from bake_end.models import Product, Category


def forwards(apps, schema_editor):
    products = Product.objects.all()
    for product in products:
        product.save()

    categories = Category.objects.all()
    for category in categories:
        category.save()


class Migration(migrations.Migration):
    dependencies = [
        ('bake_end', '0002_category_slug_alter_product_slug'),
    ]

    operations = [
        migrations.RunPython(forwards, hints={'target_db': 'default'}),
    ]
